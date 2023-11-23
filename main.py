import os
from random import randint
import subprocess
from flask import Flask, request, render_template, redirect, make_response, send_file, jsonify
from werkzeug.utils import secure_filename
import logging
import datetime

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
                logging.info(f"OCR o arquivo {UPLOAD_FOLDER}/{filename}")
                subprocess.run(['/usr/bin/ocrmypdf', '--skip-text', f'{UPLOAD_FOLDER}/{filename}', f'{OUTPUT_FOLDER}/{filename}'], check=True)
                if os.path.exists(f'{OUTPUT_FOLDER}/{filename}'):
                    '''return render_template(
                        'output.html',
                        link=f'http://127.0.0.1:8080/arquivo/{filename}'
                    )'''
                    return jsonify({'link': f'http://127.0.0.1:8080/arquivo/{filename}'})
                else:
                    return jsonify({'erro':"Não foi possível converter o pdf"})
            else:
                return jsonify({'erro':"Não é um arquivo pdf válido"})
        os.remove(f'{UPLOAD_FOLDER}/{filename}')
    except Exception as erro:
        return jsonify({'erro':f"Não foi possível converter o pdf. Erro: {erro}"})

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


