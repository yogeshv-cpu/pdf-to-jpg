import subprocess
import io
import base64
from flask import Flask, request, jsonify

subprocess.run(["apt-get", "install", "-y", "poppler-utils"], capture_output=True)

from pdf2image import convert_from_bytes

app = Flask(__name__)

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

    img_base64 = base64.b64encode(img_io.read()).decode('utf-8')

    return jsonify({
        "Files": [
            {
                "Url": f"data:image/jpeg;base64,{img_base64}"
            }
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)