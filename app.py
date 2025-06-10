from flask import Flask, request, render_template, send_file, redirect, url_for
import os
from pdf_to_epub import pdf_to_epub

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            epub_filename = file.filename.rsplit('.', 1)[0] + '.epub'
            epub_path = os.path.join(app.config['OUTPUT_FOLDER'], epub_filename)
            file.save(pdf_path)
            pdf_to_epub(pdf_path, epub_path)
            return redirect(url_for('download_file', filename=epub_filename))
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    epub_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    return send_file(epub_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
