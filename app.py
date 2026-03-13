import subprocess
import io
import uuid
import os
from flask import Flask, request, jsonify, send_file

subprocess.run(["apt-get", "install", "-y", "poppler-utils"], capture_output=True)

from pdf2image import convert_from_bytes

app = Flask(__name__)

images_store = {}

@app.route('/convert', methods=['POST'])
def convert_pdf_to_jpg():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    pdf_file = request.files['file']
    pdf_bytes = pdf_file.read()

    images = convert_from_bytes(pdf_bytes, first_page=1, last_page=1, fmt='jpeg')

    img_io = io.BytesIO()
    images[0].save(img_io, format='JPEG', quality=90)
    img_io.seek(0)

    image_id = str(uuid.uuid4())
    images_store[image_id] = img_io.read()

    base_url = os.environ.get('RENDER_EXTERNAL_URL', 'http://localhost:10000')
    image_url = f"{base_url}/image/{image_id}"

    return jsonify({
        "Files": [
            {
                "Url": image_url
            }
        ]
    })

@app.route('/image/<image_id>', methods=['GET'])
def get_image(image_id):
    if image_id not in images_store:
        return jsonify({'error': 'Image not found'}), 404
    return send_file(io.BytesIO(images_store[image_id]), mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)