# Deepfake-Detector-App
# 🧠 Deepfake Detection Web App

A Flask-based web application that detects deepfake images using a trained machine learning model. This project demonstrates how computer vision and deep learning can be used to detect manipulated (deepfake) faces in uploaded images.

---

## 📌 Features

- Upload any face image to check if it's real or fake
- Uses a trained ML model to classify deepfakes
- Simple UI built with Flask, HTML, and CSS
- Stores uploaded image history in a local database (SQLite)
- Exports detection history to CSV

---

## 🧰 Technologies Used

- **Python 3**
- **Flask** – Web application framework
- **TensorFlow / Keras** – Model inference
- **OpenCV / Pillow** – Image processing
- **SQLite** – Local database for upload history
- **HTML/CSS** – Frontend interface

---

## 📊 Model

- Model type: Convolutional Neural Network (CNN)
- Format: `.h5` (Keras saved model)
- Input shape: 128x128 or 224x224 pixels (depending on training)
- Trained using real vs. fake face datasets

---

## 📁 Project Structure

```bash
deepfake-detector/
│
├── app.py                # Flask main app
├── model/                # Contains trained model (e.g., model.h5)
├── templates/            # HTML pages
│   └── index.html
├── static/               # CSS and JS
├── uploads/              # Uploaded image folder
├── instance/             # SQLite DB file
├── import_db_to_csv.py   # Script to export database to CSV
├── requirements.txt      # Python dependencies
└── README.md             # This file


🚀 How to Run Locally
1. Clone the repository
git clone https://github.com/chandansharma7/Deepfake-Detector-App
cd deepfake-detector

2. Install dependencies:
pip install -r requirements.txt

3. Run the app:
python main.py

4.Open browser and go to:
http://127.0.0.1:5000/


