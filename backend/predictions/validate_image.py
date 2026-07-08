from PIL import Image
import os

def validateImage(file):

    valid = True
    message = "Image is valid"

    valid_extensions = [".jpg",".jpeg",".png",".webp"]
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in valid_extensions:
        message = "Unsupported file extension"
        valid = False

    try:
        img = Image.open(file)
        img.verify()
    except Exception:
        message = "Uploaded file is not a valid image"
        valid = False
    
    file.seek(0)

    return {
        "valid":valid,
        "message":message
    }

