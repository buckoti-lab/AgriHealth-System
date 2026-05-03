# AgriHealth System

### A Deep Learning-Based Vegetable Disease Detection System

## Overview

**AgriHealth System** is a web-based intelligent system that detects vegetable diseases using deep learning. The system allows users (farmers or researchers) to upload plant images and receive instant predictions about:

* Crop type
* Disease classification

It is built using Django for backend services and integrates a trained Convolutional Neural Network (CNN) model for image classification.

## Features

* Upload vegetable leaf images
* AI-powered disease detection
* Multi-output prediction (crop + disease)
* Prediction history tracking
* User authentication system
* Django admin

## AI Model

* Architecture: CNN  modal (EfficientNetB0)
* Framework: TensorFlow / Keras
* Input Size: 224 × 224 images
* Output:

  * Crop classification
  * Disease classification

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/buckoti-lab/AgriHealth-System.git
cd AgriHealth-System
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Start server

```bash
python manage.py runserver
```

## Technologies Used

* Backend: Django
* AI/ML: TensorFlow
* Frontend: HTML, CSS, JavaScript
* Database: MySQL


## License

This project is for academic and research purposes.


## Project Team
This project was developed as part of a Final Year Project (FYP) focusing on applying Artificial Intelligence in Agriculture

## Authors

**Buckoti**
**Jastin**
**Alfred**
**Joshua**
**Ngwandu**