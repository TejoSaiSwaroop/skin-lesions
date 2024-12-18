from flask import Flask, request, jsonify, send_from_directory
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Load the saved model
model = load_model('skin_lesion_classifier.h5')

# List of labels based on your training data
labels = ['Acne and Rosacea Photos', 'Actinic Keratosis Basal Cell Carcinoma and other Malignant Lesions', 'Atopic Dermatitis Photos', 'Bullous Disease Photos', 'Cellulitis Impetigo and other Bacterial Infections', 'Eczema Photos', 'Exanthems and Drug Eruptions', 'Hair Loss Photos Alopecia and other Hair Diseases', 'Herpes HPV and other STDs Photos', 'Light Diseases and Disorders of Pigmentation', 'Lupus and other Connective Tissue diseases', 'Melanoma Skin Cancer Nevi and Moles', 'Nail Fungus and other Nail Disease', 'Poison Ivy Photos and other Contact Dermatitis', 'Psoriasis pictures Lichen Planus and related diseases', 'Scabies Lyme Disease and other Infestations and Bites', 'Seborrheic Keratoses and other Benign Tumors', 'Systemic Disease', 'Tinea Ringworm Candidiasis and other Fungal Infections', 'Urticaria Hives', 'Vascular Tumors', 'Vasculitis Photos', 'Warts Molluscum and other Viral Infections']

def predict_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.
    predictions = model.predict(img_array)
    predicted_class_idx = np.argmax(predictions[0])
    predicted_class = labels[predicted_class_idx]
    return predicted_class

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/style.css')
def css():
    return send_from_directory('.', 'style.css')

@app.route('/predict', methods=['POST'])
def upload_file():
    file = request.files['file']
    file_path = './' + file.filename
    file.save(file_path)
    prediction = predict_image(file_path)
    return jsonify({'prediction': prediction})

@app.route('/get_info/<class_name>')
def get_info(class_name):
    url = f"https://en.wikipedia.org/wiki/{class_name.replace(' ', '_')}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the paragraphs in the content
    paragraphs = soup.find_all('p')
    content = "\n".join([para.get_text() for para in paragraphs[:3]])  # Get first 3 paragraphs as summary

    return jsonify({'info': content})

if __name__ == '__main__':
    app.run(debug=True)
