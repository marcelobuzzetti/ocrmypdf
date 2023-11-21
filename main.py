import os
import ocrmypdf
from random import randint
import multiprocessing
from flask import Flask, request, render_template, redirect, make_response, send_file, jsonify
from werkzeug.utils import secure_filename
import logging
import datetime
import time
from flask_socketio import SocketIO

UPLOAD_FOLDER = 'uploaded'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'pdf'}
logging.basicConfig( level=logging.INFO)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def perform_ocr(input_file, output_file):
    ocrmypdf.ocr(input_file, output_file, deskew=True, language='por')
    os.remove(input_file)
    socketio.emit('ocr_completed', {'message': 'OCR process completed'})
    socketio.emit('output_file', {'link': f'/arquivo/{output_file}'})


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
                #time.sleep(10)
                try:
                    logging.info(f"OCR o arquivo {UPLOAD_FOLDER}/{filename}")
                    #ocrmypdf.ocr(f'{UPLOAD_FOLDER}/{filename}', f'{OUTPUT_FOLDER}/{filename}', deskew=True, language='por')
                    #perform_ocr(f'{UPLOAD_FOLDER}/{filename}', f'{OUTPUT_FOLDER}/{filename}')
                    ocr_process = multiprocessing.Process(target=perform_ocr, args=(f'{UPLOAD_FOLDER}/{filename}', f'{OUTPUT_FOLDER}/{filename}'))
                    ocr_process.start()
                    logging.info(f"Removendo o arquivo {UPLOAD_FOLDER}/{filename}")
                    #os.remove(f'{UPLOAD_FOLDER}/{filename}')
                    #return send_file(f'{OUTPUT_FOLDER}/{filename}', as_attachment=True)
                except Exception as erro:
                    logging.critical(erro)
                    logging.info(f"Removendo o arquivo {UPLOAD_FOLDER}/{filename}")
                    #os.remove(f'{UPLOAD_FOLDER}/{filename}')
                    return f"Não foi possível converter o pdf devido ao seguinte erro:\n {erro}"
            return render_template(
                'output.html',
                link=filename
            )
    except Exception as erro:
        return f"Não foi possível converter o pdf devido ao seguinte erro:\n {erro}"

@socketio.on('start_ocr')
def start_ocr(data):
    input_file = 'input.pdf'  # Replace with your input PDF file
    output_file = 'output.pdf'  # Replace with your desired output file
    ocr_process = multiprocessing.Process(target=perform_ocr, args=(input_file, output_file))
    ocr_process.start()

@app.route("/arquivo/<file>", methods=['GET'])
def arquivo(file):
    return send_file(f'{OUTPUT_FOLDER}/{file}', as_attachment=True)

if __name__ == '__main__':
    #app.run(port=8080, debug=True)
    socketio.run(app, port=8080, debug=True)


