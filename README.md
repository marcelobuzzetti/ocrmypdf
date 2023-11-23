# Sistema para tornar o PDF 'PESQUISÁVEL' #

Sistema feito para ser usado no Linux

# Instalações necessárias #

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