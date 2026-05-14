from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response

from django.utils.timesince import timesince
from django.utils.timezone import now
from datetime import timedelta

from .models import Prediction
from .utils import predict_image
from .validate_image import validateImage

from images.models import Image as I
from crops.models import Vegetable as V
from diseases.models import Disease as D
from treatments.models import Treatment as T


    
data = []

# ============================
# Helper: Get Treatments
# ============================
def get_treatments(disease):
    treatments = T.objects.filter(disease=disease)

    return [
        {
            "solution": t.solution,
            "prevention": t.prevention
        }
        for t in treatments
    ]


# ============================
# Predict Endpoint
# ============================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def predict(request):
    image = request.FILES.get('image')

    if not image:
        return Response({"error": "No image provided"}, status=400)

    validate = validateImage(image)

    if validate['valid'] is False:
        return Response({
            "success":False,
            "message":validate['message']
        })

    # Save uploaded image
    uploaded_image = I.objects.create(
        name=image.name,
        uploaded_by=request.user,
        image_file=image
    )

    # Run AI prediction
    path = uploaded_image.image_file.path

    result = predict_image(path)

    if result["label"] == "unknown":
        data.append({
            "vegetable": None,
            "disease": None,
            "crop_confidence": None,
            "disease_confidence": None,
            "image_url": uploaded_image.image_file.url,
            "treatments": []
        })

        # Response  
        return Response({
            "success": True,
            "unknown": True,
            "message": "Unknown crop or disease detected.",
            "data": data
        })

    # Get or create DB records
    veg, _ = V.objects.get_or_create(name=result["crop"])
    dis, _ = D.objects.get_or_create(
        name=result["disease"],
        vegetable=veg
    )

    # Get treatments
    treatment_data = get_treatments(dis)

    # Save prediction history
    Prediction.objects.create(
        user=request.user,
        image=uploaded_image,
        vegetable=veg,
        disease=dis,
        crop_confidence=result["crop_confidence"],
        disease_confidence=result["disease_confidence"],
    )

    # Response  
    data.append({
        "vegetable": veg.name,
        "disease": dis.name,
        "crop_confidence": result["crop_confidence"],
        "disease_confidence": result["disease_confidence"],
        "image_url": uploaded_image.image_file.url,
        "treatments": treatment_data 
    })

    return Response({
        "success":True,
        "data":data
    })


# ============================
# History Endpoint
# ============================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def history(request):
    predictions = Prediction.objects.filter(
        user=request.user
    ).order_by('-created_at')

    for p in predictions:
        treatment_data = get_treatments(p.disease)

        diff = now() - p.created_at

        if diff < timedelta(minutes=1):
            time_display = "now"
        else:
            time_display = timesince(p.created_at).split(',')[0] + " ago"

        data.append({
            "id": p.id,
            "image": p.image.image_file.url if p.image.image_file else None,
            "vegetable": p.vegetable.name,
            "disease": p.disease.name,
            "date": p.created_at.isoformat(),
            "confidence": float(p.disease_confidence),
            # "crop_confidence": float(result["crop_confidence"]),
            # "disease_confidence": float(result["disease_confidence"]),
            "time_ago": time_display,
            "treatments": treatment_data
        })

    return Response({
        "success":True,
        "data":data
    })

# ============================
# Recent Endpoint
# ============================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recent(request):
    predictions = Prediction.objects.filter(
        user=request.user
    ).order_by('-created_at')[:3]

    data = []

    for p in predictions:
        treatment_data = get_treatments(p.disease)

        diff = now() - p.created_at

        if diff < timedelta(minutes=1):
            time_display = "now"
        else:
            time_display = timesince(p.created_at).split(',')[0] + " ago"

        data.append({
            "id": p.id,
            "image": p.image.image_file.url if p.image.image_file else None,
            "vegetable": p.vegetable.name,
            "disease": p.disease.name,
            "date": p.created_at.isoformat(),
            "time_ago": time_display,
            "confidence": float(p.disease_confidence),
            "treatments": treatment_data
        })

    return Response({
        "success":True,
        "data":data
    })


# ============================
# Delete Prediction Endpoint
# ============================
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete(request, pk):
    try:
        prediction = Prediction.objects.get(id=pk, user=request.user)
        prediction.delete()
        return Response({
            "success": True,
            "message": "Prediction deleted successfully"
        })
    except Prediction.DoesNotExist:
        return Response({
            "success": False,
            "error": "Prediction not found"
        }, status=404)