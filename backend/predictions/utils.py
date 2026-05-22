import numpy as np
import json
import os
from PIL import Image
import backend.settings as settings
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.efficientnet_v2 import preprocess_input
from tensorflow.keras.models import load_model

from .energy_detector import EnergyBasedUnknownDetector

# Load model
model = load_model("models/efficientnetv2_logits_100.keras")
# model = load_model("models/last_model_e100.keras")

detector = EnergyBasedUnknownDetector(model)

# # Load thresholds
# detector.crop_energy_threshold = float(np.load("models/crop_threshold.npy"))
# detector.disease_energy_threshold = float(np.load("models/disease_threshold.npy"))

# Load labels
with open("models/labels.json") as f:
    labels = json.load(f)

# Reverse mappings
crop_classes = {v: k for k, v in labels["crop"].items()}
disease_classes = {v: k for k, v in labels["disease"].items()}

def predict_image(filename):

    img = load_img(filename, target_size=(224, 224))
    img_array = img_to_array(img)

    img_array = preprocess_input(img_array)

    # Use detector instead of raw model
    result = detector.predict_with_unknown(
        img_array,
        crop_labels=crop_classes,
        disease_labels=disease_classes,
        return_details=True
    )

    # UNKNOWN case
    if result["is_unknown"]:
        return {
            "crop": None,
            "disease": None,
            "crop_confidence": None,
            "disease_confidence": None,
            "label": "unknown",
            "img_url": filename
        }

    # KNOWN case 
    return {
        "crop": result["crop"],
        "disease": result["disease"],
        "crop_confidence": result["crop_confidence"],
        "disease_confidence": result["disease_confidence"],
        "label": result["label"],
        "img_url": filename
    }


# def predict_image(filename):

#     img = load_img(filename, target_size=(224,224))
#     img_array = img_to_array(img)
   
#     img_array = preprocess_input(img_array)
#     img_array = np.expand_dims(img_array, axis=0)

#     #Multi-output prediction
#     crop_pred, disease_pred = model.predict(img_array)

#     crop_idx = np.argmax(crop_pred)
#     disease_idx = np.argmax(disease_pred)

#     crop = crop_classes[crop_idx]
#     disease = disease_classes[disease_idx]

#     crop_conf = float(np.max(crop_pred))
#     disease_conf = float(np.max(disease_pred))

#     return {
#         "crop": crop,
#         "disease": disease,
#         "crop_confidence": crop_conf,
#         "disease_confidence": disease_conf,
#         "label": "",
#         "img_url": filename
#     }