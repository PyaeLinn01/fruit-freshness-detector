from flask import Flask, request, jsonify
import torch
import torch.nn as nn
import numpy as np
from torchvision import transforms
import cv2
from net import Net  # Ensure you have the Net model definition available
import os

app = Flask(__name__)
ML_MODEL = None
current_dir = os.path.dirname(os.path.abspath(__file__))
ML_MODEL_FILE = os.path.join(current_dir, "model.pt")
TORCH_DEVICE = "cpu"

def get_model():
    """Loading the ML model once and returning the ML model"""
    global ML_MODEL
    if not ML_MODEL:
        if not os.path.exists(ML_MODEL_FILE):
            raise FileNotFoundError(f"Model file '{ML_MODEL_FILE}' not found. Please ensure it is in the correct directory.")
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
    model = get_model()
    if model is None:
        return None
    out = model(batch)
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
    if freshness_percentage is None:
        return None
    return {
        "freshness_level": freshness_percentage,
        "price": int(freshness_percentage / 100 * 10000)
    }

@app.route('/api/recognize', methods=["POST"])
def api_recognize():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    cv_image = imdecode_image(request.files["image"])
    fruit_information = recognize_fruit_by_cv_image(cv_image)
    if fruit_information is not None:
        return jsonify(fruit_information)
    else:
        return jsonify({"error": "An error occurred while processing the image"}), 500

if __name__ == "__main__":
    app.run(debug=True)
