# Imports
import fitz
import os
import torch
from torchvision import transforms, models
from PIL import Image
import imagehash
from sklearn.metrics import precision_score, recall_score
from sklearn.utils.class_weight import compute_class_weight
import numpy as np
from datetime import datetime
import io
import shutil
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import Flask-CORS

app = Flask(__name__)
CORS(app)  # Aktivieren von CORS für die gesamte App

# Funktion zum Extrahieren von Bildern aus einem PDF
def extract_images_from_pdf(pdf_data, output_folder):
    pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
    for i in range(len(pdf_document)):
        for img_index, img in enumerate(pdf_document.get_page_images(i)):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            
            
            image = image.convert("RGB")
            
            image.save(os.path.join(output_folder, f"page_{i + 1}_img_{img_index + 1}.png"))


# Funktion zum Laden des Modells
def load_model(model_path):
    model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
    num_ftrs = model.fc.in_features
    model.fc = torch.nn.Linear(num_ftrs, 2) 
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model.load_state_dict(torch.load(model_path, map_location=device))
    model = model.to(device)
    model.eval()
    return model

# Bildvorbereitung
def preprocess_image(image_path):
    transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,)),
    ])
    image = Image.open(image_path).convert('RGB')
    image = transform(image)
    image = image.unsqueeze(0)  # Batch-Dimension hinzufügen
    return image

# Vorhersage machen und Wahrscheinlichkeiten zurückgeben
def predict_proba(model, image_tensor):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    image_tensor = image_tensor.to(device)
    with torch.no_grad():
        output = model(image_tensor)
        probabilities = torch.nn.functional.softmax(output, dim=1)
    return probabilities.cpu().numpy()

# Funktion zum Erstellen von Image-Hashes   
def get_image_hash(image_path):
    image = Image.open(image_path)
    return imagehash.average_hash(image)

# Funktion zum Laden der Hashes von dontValidate-Bildern
def load_dont_validate_hashes(folder_path):
    hashes = set()
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(folder_path, filename)
            img_hash = get_image_hash(image_path)
            hashes.add(img_hash)
    return hashes

# Funktion zum Auswerten und Kopieren von Bildern basierend auf den Vorhersagen
def evaluate_and_return_images(model, folder_path, dont_validate_hashes):
    results = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(folder_path, filename)
            img_hash = get_image_hash(image_path)
            if img_hash in dont_validate_hashes:
                continue

            image_tensor = preprocess_image(image_path)
            probabilities = predict_proba(model, image_tensor)
            positive_prob = float(probabilities[0][1])  # Wahrscheinlichkeit für die Klasse 'positive' als float umwandeln
            result = {
                "name": filename,
                "probability_positive": positive_prob,
                "image": None  # Bild wird später hinzugefügt
            }
            with open(image_path, "rb") as img_file:
                result["image"] = base64.b64encode(img_file.read()).decode('utf-8')
            results.append(result)
    return results

# Flask-Route zum Hochladen und Verarbeiten eines PDFs
@app.route('/process_pdf', methods=['POST'])
def process_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file provided"}), 400
    pdf_data = file.read()

    # Temporäre Ordner erstellen
    export_folder = "temp/exported_images"
    dont_validate_folder = "resources/dontValidate"
    os.makedirs(export_folder, exist_ok=True)
    os.makedirs(dont_validate_folder, exist_ok=True)

    # Extrahiere Bilder aus PDF
    extract_images_from_pdf(pdf_data, export_folder)

    # dontValidate-Hashes laden
    dont_validate_hashes = load_dont_validate_hashes(dont_validate_folder)

    # Modellpfad
    model_path = "resources/model/model.pth"

    # Modell laden
    model = load_model(model_path)

    # Bilder auswerten und Ergebnisse sammeln
    results = evaluate_and_return_images(model, export_folder, dont_validate_hashes)

    # Aufräumen
    shutil.rmtree("temp")

    return jsonify(results)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
