from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes, api_view
from django.core.files.storage import FileSystemStorage
import os

from .models import Prediction
from rest_framework.response import Response
from .utils import predict_image
from images.models import Image as I
from crops.models import Vegetable as V
from diseases.models import Disease as D
from treatments.models import Treatment as T

import backend.settings as settings


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def predict(request):
    image = request.FILES.get('image')

    # 1️⃣ Check if image is in request
    # image_file = request.FILES.get('image')
    if not image:
        return Response({"error": "No image provided"}, status=400)

    # fs = FileSystemStorage()
    # filename = fs.save(image.name, image)
    # path = fs.path(filename)

    # 2️⃣ Save the file using FileSystemStorage
    
    # fs = FileSystemStorage(location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL)
    # filename = fs.save(image_file.name, image_file)
    # file_url = fs.url(filename)
    # filename = image_file.name
    # filepath = os.path.join('media', 'uploads','predictions',filename)  
    # image_file.save(filepath)

    # image.name = new_name

    uploaded_image = I.objects.create(
        name=image.name,
        uploaded_by=request.user,
        image_file=image
    )

    
    # ✅ Get file path for AI
    path = uploaded_image.image_file.path
    
    result = predict_image(path)

    veg, _ = V.objects.get_or_create(name=result["crop"])
    dis, _ = D.objects.get_or_create(
        name=result["disease"],
        vegetable=veg
    )

    treatments = T.objects.filter(disease=dis)

    if treatments.exists():
        treatment_data = [
            {
                "solution": t.solution,
                "prevention": t.prevention
            }
            for t in treatments
        ]
    else:
        treatment_data = "No published treatments for such disease"

    Prediction.objects.create(
        user=request.user,
        image=uploaded_image, 
        vegetable=veg,
        disease=dis,
        crop_confidence=result["crop_confidence"],
        disease_confidence=result["disease_confidence"],
    )

    return Response(result)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def history(request):
#     predictions = Prediction.objects.filter(user=request.user).order_by('-created_at')

#     data = []
#     for p in predictions:
#         data.append({
#             "image": p.image.image_file,
#             "vegetable": p.vegetable.name,
#             "disease": p.disease.name,
#             "date": p.created_at,
#             "confidence": p.disease_confidence
#         })

#     return Response(data)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def history(request):
    predictions = Prediction.objects.filter(user=request.user).order_by('-created_at')

    data = []
    for p in predictions:
        data.append({
            "image": p.image.image_file.url if p.image.image_file else None,
            "vegetable": p.vegetable.name,
            "disease": p.disease.name,
            "date": p.created_at.isoformat(),  # ✅ FIX datetime
            "confidence": float(p.disease_confidence)
            "treatments": treatment_data
        })
    return Response(data)