import tensorflow as tf
import numpy as np
import json
import os
from PIL import Image
import backend.settings as settings
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.resnet50 import preprocess_input

# Load model
model = tf.keras.models.load_model("cnn_assets/model.keras")

# Load labels
with open("cnn_assets/labels.json") as f:
    labels = json.load(f)

# Reverse mappings
crop_classes = {v: k for k, v in labels["crop"].items()}
disease_classes = {v: k for k, v in labels["disease"].items()}


def predict_image(filename):

    img = load_img(filename, target_size=(224,224))
    img_array = img_to_array(img)
   

    img_array = preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)

    #Multi-output prediction
    crop_pred, disease_pred = model.predict(img_array)

    crop_idx = np.argmax(crop_pred)
    disease_idx = np.argmax(disease_pred)

    crop = crop_classes[crop_idx]
    disease = disease_classes[disease_idx]

    crop_conf = float(np.max(crop_pred))
    disease_conf = float(np.max(disease_pred))

    return {
        "crop": crop,
        "disease": disease,
        "crop_confidence": crop_conf,
        "disease_confidence": disease_conf,
        "img_url":filename
    }