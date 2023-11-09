import os
import ocrmypdf
from random import randint
from flask import Flask, request, render_template, redirect, make_response, send_file
from werkzeug.utils import secure_filename
import logging
import datetime

UPLOAD_FOLDER = 'uploaded'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'pdf'}
logging.basicConfig( level=logging.INFO)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def api_live():
    logging.info(f"Acesso em {datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}")
    if request.method == "GET":
        return render_template('index.html')
    if request.method == "POST":
        if 'pdf' not in request.files:
            return redirect(request.url)
        file = request.files['pdf']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = f"{randint(0, 100)}_{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}_{secure_filename(file.filename)}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            try:
                ocrmypdf.ocr(f'{UPLOAD_FOLDER}/{filename}', f'{OUTPUT_FOLDER}/{filename}', deskew=True, language='por')
                return send_file(f'{OUTPUT_FOLDER}/{filename}', as_attachment=True)
            except Exception as erro:
                logging.critical(erro)

@app.route("/arquivo/<file>", methods=['GET'])
def arquivo(file):
    return send_file(f'{OUTPUT_FOLDER}/{file}', as_attachment=True)

if __name__ == '__main__':
    app.run(port=8080, debug=True)

