# Sistema para tornar o PDF 'PESQUISÁVEL' #

Sistema feito para ser usado no Linux

# Pacotes necessários no Linux #

ocrmypdf

tesseract-ocr-por

automake

libtool

libleptonica-dev git

JBIG2 encoder

# Instalando o JBIG2 encoder #
``` 
git clone https://github.com/agl/jbig2enc
cd jbig2enc
./autogen.sh 
./configure && make 
[sudo] make install
```

## Rodando sem container ##
Execute `pip install -r requirements.txt`
* Execute local:
```
env FLASK_APP=main.py gunicorn -w 4 --bind 0.0.0.0:8080 --timeout 600 main:app
```

## Rodando com container ##
Faça o build da imagem
```
docker build -t ocrmypdf .
```
Execute o container no modo interativo
```
docker run -d -p 8080:8080 ocrmypdf
```

# Referencias Tecnicas
* https://ocrmypdf.readthedocs.io/en/latest/installation.html
* https://ocrmypdf.readthedocs.io/en/latest/jbig2.html#jbig2
* https://gunicorn.org/