from flask import Flask, request, render_template, redirect, url_for, session
from PIL import Image
import os
import io
import tempfile
import pytesseract

try:
    from pdf2image import convert_from_path
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False
    print("Warning: pdf2image not installed. PDF support disabled.")

try:
    # Test if tesseract is available
    pytesseract.get_tesseract_version()
    TESSERACT_AVAILABLE = True
    print("✓ Tesseract OCR is ready")
except Exception as e:
    TESSERACT_AVAILABLE = False
    print(f"✗ Tesseract error: {e}")

app = Flask(__name__, template_folder='templates')
app.secret_key = 'ocr_secret_key_123'


@app.route("/", methods=["GET", "POST"])
def index():
    result_text = ""
    error_msg = ""

    if request.method == "POST":
        if "file" not in request.files:
            error_msg = "Please select a file"
        else:
            file = request.files["file"]
            
            if file.filename == "":
                error_msg = "No file selected"
            else:
                try:
                    content = file.read()
                    filename = file.filename.lower()
                    
                    if not TESSERACT_AVAILABLE:
                        error_msg = "Tesseract OCR is not available"
                    else:
                        # Handle PDF files
                        if filename.endswith('.pdf'):
                            if not PDF_SUPPORT:
                                error_msg = "PDF support requires pdf2image package"
                            else:
                                try:
                                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                                        tmp.write(content)
                                        tmp_path = tmp.name
                                    
                                    try:
                                        images = convert_from_path(tmp_path, dpi=300)
                                        all_text = []
                                        
                                        for image in images:
                                            text = pytesseract.image_to_string(image, lang="eng")
                                            if text.strip():
                                                all_text.append(text)
                                        
                                        if all_text:
                                            result_text = "\n\n--- Page Break ---\n\n".join(all_text)
                                        else:
                                            error_msg = "No text detected in PDF"
                                    finally:
                                        os.remove(tmp_path)
                                except Exception as e:
                                    error_msg = f"PDF processing error: {str(e)}"
                        
                        # Handle image files
                        else:
                            try:
                                image = Image.open(io.BytesIO(content))
                                result_text = pytesseract.image_to_string(image, lang="eng")
                                if not result_text.strip():
                                    error_msg = "No text detected in image"
                            except Exception as e:
                                error_msg = f"Tesseract error: {str(e)}"
                            
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
        
        # Store result in session to display after redirect
        session['result_text'] = result_text
        session['error_msg'] = error_msg
        return redirect(url_for('index'))
    
    # Get result from session if available
    if 'result_text' in session:
        result_text = session.pop('result_text', '')
    if 'error_msg' in session:
        error_msg = session.pop('error_msg', '')

    return render_template("index.html", text=result_text, error=error_msg)


if __name__ == "__main__":
    # For local development
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
