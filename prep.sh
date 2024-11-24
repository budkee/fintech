#!/bin/sh

echo " "
echo "Iniciando a aplicação..."

export PATH="$PATH:/home/zimute/.local/bin"

# Atualizar o gerenciador de pacotes pip
pip install --upgrade pip

# Instalando dependências
if [ -f "requirements.txt" ]; then
    echo " "
    echo ">>> Instalando dependências... <<<"
    echo " "
    pip install -r requirements.txt
else
    echo " "
    echo ">>> Arquivo requirements.txt não encontrado. Verifique o arquivo requirements.txt. >>>"
fi

echo " "

