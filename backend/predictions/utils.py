import numpy as np
import json
import os
from PIL import Image
import backend.settings as settings
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.efficientnet_v2 import preprocess_input

from .ood_detector import UnifiedUnknownDetector


# Load labels
with open("models/labels.json") as f:
    labels = json.load(f)


crop_classes = {v: k for k, v in labels["crop"].items()}
disease_classes = {v: k for k, v in labels["disease"].items()}

def predict_image(filename,model,load_dir):
    # model = load_model("models/v3/efficientNetV2_B0.keras")
    # load_dir = "models/v3/"

    detector = UnifiedUnknownDetector(model,load_dir)

    img = load_img(filename, target_size=(224, 224))
    img_array = img_to_array(img)

    img_array = preprocess_input(img_array)

    # Use detector instead of raw model
    result = detector.predict(img_array,crop_labels=crop_classes,disease_labels=disease_classes,return_details=True)

    return result