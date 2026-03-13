from flask import Flask, request, jsonify, send_file
from pdf2image import convert_from_bytes
import io

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

    return send_file(img_io, mimetype='image/jpeg', download_name='output.jpg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
```

---

**`requirements.txt`**
```
flask
pdf2image
pillow