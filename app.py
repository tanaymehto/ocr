from flask import Flask, request, jsonify
from flask_cors import CORS
from google.cloud import vision
from PIL import Image
import os
import io
import tempfile

try:
    from pdf2image import convert_from_path
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False
    print("Warning: pdf2image not installed. PDF support disabled.")

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
    print("✓ Tesseract OCR is ready")
except ImportError:
    TESSERACT_AVAILABLE = False
    print("✗ Tesseract not available")

# Set credentials
if os.path.exists('credentials.json'):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'
elif os.environ.get('GOOGLE_CREDENTIALS_JSON'):
    # Create a temporary file for credentials from environment variable
    # This is needed because Google Client expects a file path
    import json
    
    cred_content = os.environ.get('GOOGLE_CREDENTIALS_JSON')
    try:
        # Verify it's valid JSON
        json.loads(cred_content)
        
        # Write to a temporary file
        fd, path = tempfile.mkstemp()
        with os.fdopen(fd, 'w') as tmp:
            tmp.write(cred_content)
        
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path
        print("✓ Google Cloud credentials loaded from environment")
    except Exception as e:
        print(f"✗ Error loading credentials from environment: {e}")

try:
    client = vision.ImageAnnotatorClient()
    print("✓ Google Cloud Vision API is ready")
except Exception as e:
    print(f"✗ Vision API error: {e}")
    client = None

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests


@app.route('/extract', methods=['POST'])
def extract_text():
    """API endpoint for text extraction"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    engine = request.form.get('engine', 'google')  # Default to Google Vision
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Validate engine choice
    if engine == 'google' and not client:
        return jsonify({'error': 'Google Vision API not initialized'}), 500
    
    if engine == 'tesseract' and not TESSERACT_AVAILABLE:
        return jsonify({'error': 'Tesseract not available'}), 500
    
    try:
        content = file.read()
        filename = file.filename.lower()
        result_text = ""
        
        # Handle PDF files
        if filename.endswith('.pdf'):
            if not PDF_SUPPORT:
                return jsonify({'error': 'PDF support requires pdf2image package'}), 500
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                tmp.write(content)
                tmp_path = tmp.name
            
            try:
                images = convert_from_path(tmp_path, dpi=300)
                all_text = []
                
                for image in images:
                    if engine == 'google':
                        # Convert PIL image to bytes for Google Vision
                        img_byte_arr = io.BytesIO()
                        image.save(img_byte_arr, format='PNG')
                        img_content = img_byte_arr.getvalue()
                        
                        vision_image = vision.Image(content=img_content)
                        response = client.document_text_detection(image=vision_image)
                        
                        if response.full_text_annotation:
                            all_text.append(response.full_text_annotation.text)
                        elif response.text_annotations:
                            all_text.append("\n".join([t.description for t in response.text_annotations[1:]]))
                    else:  # Tesseract
                        text = pytesseract.image_to_string(image)
                        if text.strip():
                            all_text.append(text)
                
                if all_text:
                    result_text = "\n\n--- Page Break ---\n\n".join(all_text)
                else:
                    return jsonify({'error': 'No text detected in PDF'}), 400
            finally:
                os.remove(tmp_path)
        
        # Handle image files
        else:
            if engine == 'google':
                vision_image = vision.Image(content=content)
                response = client.document_text_detection(image=vision_image)
                
                if response.full_text_annotation:
                    result_text = response.full_text_annotation.text
                elif response.text_annotations:
                    result_text = "\n".join([t.description for t in response.text_annotations[1:]])
                else:
                    return jsonify({'error': 'No text detected in image'}), 400
            else:  # Tesseract
                image = Image.open(io.BytesIO(content))
                result_text = pytesseract.image_to_string(image)
                if not result_text.strip():
                    return jsonify({'error': 'No text detected in image'}), 400
        
        return jsonify({'text': result_text, 'engine': engine}), 200
    
    except Exception as e:
        return jsonify({'error': f'Processing error: {str(e)}'}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'tesseract': TESSERACT_AVAILABLE}), 200


if __name__ == "__main__":
    # For local development
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
