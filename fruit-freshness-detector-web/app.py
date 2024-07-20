import streamlit as st
import torch
import torch.nn as nn
import numpy as np
from torchvision import transforms
import cv2
from PIL import Image
from net import Net  # Ensure you have the Net model definition available

# Load the model
ML_MODEL = None
ML_MODEL_FILE = "model.pt"
TORCH_DEVICE = "cpu"

def get_model():
    """Loading the ML model once and returning the ML model"""
    global ML_MODEL
    if not ML_MODEL:
        ML_MODEL = Net()
        ML_MODEL.load_state_dict(
            torch.load(ML_MODEL_FILE, map_location=torch.device(TORCH_DEVICE))
        )
        ML_MODEL.eval()
    return ML_MODEL

def freshness_label(freshness_percentage):
    if freshness_percentage > 90:
        return "It is really fresh, so you can eat it now!"
    elif freshness_percentage > 65:
        return "It is good, you can still enjoy it."
    elif freshness_percentage > 50:
        return "It is fair, consider eating it soon."
    elif freshness_percentage > 0:
        return "It is poor, you might want to eat it quickly."
    else:
        return "It is rotten, do not eat it."

def freshness_percentage_by_cv_image(cv_image):
    mean = (0.7369, 0.6360, 0.5318)
    std = (0.3281, 0.3417, 0.3704)
    transformation = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean, std)
    ])
    image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (32, 32))
    image_tensor = transformation(image)
    batch = image_tensor.unsqueeze(0)
    out = get_model()(batch)
    s = nn.Softmax(dim=1)
    result = s(out)
    return int(result[0][0].item() * 100)

def imdecode_image(image_file):
    return cv2.imdecode(
        np.frombuffer(image_file.read(), np.uint8),
        cv2.IMREAD_UNCHANGED
    )

def recognize_fruit_by_cv_image(cv_image):
    freshness_percentage = freshness_percentage_by_cv_image(cv_image)
    return {
        "freshness_percentage": freshness_percentage,
    }

# Streamlit app
st.title("Fruit Freshness Detector")

uploaded_file = st.file_uploader("Choose an image...", type="jpg")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    st.write("")
    st.write("Classifying...")

    cv_image = np.array(image.convert('RGB'))
    fruit_information = recognize_fruit_by_cv_image(cv_image)
    freshness_percentage = fruit_information["freshness_percentage"]

    st.write(f"Freshness Percentage: {freshness_percentage}%")
    st.write(f"Freshness Label: {freshness_label(freshness_percentage)}")
