#!/bin/bash

# Atualiza o sistema
sudo apt-get update
sudo apt-get upgrade

# Atualiza os pacotes usados no programa
sudo apt-get install python3-pip
sudo apt-get install python3-tk

# Atualiza o pip
pip3 install --upgrade pip
pip3 install customtkinter
pip3 install openmesh

echo "Atualização concluída!"