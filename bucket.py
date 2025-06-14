from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore, storage
import uuid
import os

# Firebase init
cred = credentials.Certificate("asxx.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'asxx-e8e2e.firebasestorage.app'  # Өз bucket атауыңызды жазыңыз
})
db = firestore.client()
bucket = storage.bucket()

# Flask app init
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB дейін рұқсат

# 🔹 Жалпы функция: файлды жүктеу
def upload_to_storage(file, folder):
    filename = f"{folder}/{uuid.uuid4().hex}_{file.filename}"
    blob = bucket.blob(filename)
    blob.upload_from_file(file, content_type=file.content_type)
    blob.make_public()
    return blob.public_url

# 📸 Сурет жүктеу маршруты
@app.route('/upload/image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'Файл жіберілмеген'}), 400
    
    file = request.files['file']
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        return jsonify({'error': 'Бұл сурет форматы емес'}), 400
    
    url = upload_to_storage(file, 'images')
    return jsonify({'image_url': url}), 201

# 🎥 Видео жүктеу маршруты
@app.route('/upload/video', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({'error': 'Файл жіберілмеген'}), 400
    
    file = request.files['file']
    if not file.filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        return jsonify({'error': 'Бұл видео форматы емес'}), 400
    
    url = upload_to_storage(file, 'videos')
    return jsonify({'video_url': url}), 201

# 📄 Құжат жүктеу маршруты
@app.route('/upload/document', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        return jsonify({'error': 'Файл жіберілмеген'}), 400
    
    file = request.files['file']
    if not file.filename.lower().endswith(('.pdf', '.doc', '.docx', '.txt', '.pptx')):
        return jsonify({'error': 'Бұл құжат форматы емес'}), 400
    
    url = upload_to_storage(file, 'documents')
    return jsonify({'document_url': url}), 201

# 🚀 Серверді іске қосу
if __name__ == '__main__':
    app.run(debug=True)
