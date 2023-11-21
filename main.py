import os
import ocrmypdf
from random import randint
import multiprocessing
from flask import Flask, request, render_template, redirect, make_response, send_file, jsonify
from werkzeug.utils import secure_filename
import logging
import datetime
import time

UPLOAD_FOLDER = 'uploaded'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'pdf'}
logging.basicConfig( level=logging.INFO)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'secret'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def perform_ocr(input_file, output_file):
    ocrmypdf.ocr(input_file, output_file, deskew=True, language='por')
    os.remove(input_file)


@app.route("/", methods=['GET', 'POST'])
def api_live():
    try:
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
                filename = f"{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}_{randint(0, 100)}_{secure_filename(file.filename)}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                try:
                    logging.info(f"OCR o arquivo {UPLOAD_FOLDER}/{filename}")
                    ocr_process = multiprocessing.Process(target=perform_ocr, args=(f'{UPLOAD_FOLDER}/{filename}', f'{OUTPUT_FOLDER}/{filename}'))
                    ocr_process.start()
                except Exception as erro:
                    logging.critical(erro)
                    return f"Não foi possível converter o pdf devido ao seguinte erro:\n {erro}"
            return render_template(
                'output.html',
                link=f'http://127.0.0.1:8080/arquivo/{filename}'
            )
    except Exception as erro:
        return f"Não foi possível converter o pdf devido ao seguinte erro:\n {erro}"

@app.route("/arquivo/<file>", methods=['GET'])
def arquivo(file):
    try:
        return send_file(f'{OUTPUT_FOLDER}/{file}', as_attachment=True)
    except:
        return render_template(
                'output.html',
                link=file
            )

if __name__ == '__main__':
    app.run(port=8080, debug=True)


