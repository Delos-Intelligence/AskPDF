import requests
import os
import json
import base64
import time
import sys

CHUNK_SIZE = 4096  # 4KB, vous pouvez ajuster cette taille selon vos besoins
URL = 'http://localhost:8000/upload/'
ASK_URL = 'http://localhost:8000/ask/'

REMOTE_URL = 'https://delosaskpdf-b71e417edc56.herokuapp.com/upload/'
REMOTE_ASK_URL = 'https://delosaskpdf-b71e417edc56.herokuapp.com/ask/'

PATH = "/Users/pierredgr/Documents/Business/Actuels/Delos/NUKEMA/CCTP.pdf" # Remplacer par un fichier test

def send_chunks(file_path : str = PATH):
    print("Beginning sending the doc")
    i = 0
    with open(file_path, 'rb') as pdf_file:
        file_size = os.path.getsize(file_path)
        file_info = {
                'user_id' : "1345",
                'title' : "test_file",
                "type":".pdf",
                "size":str(file_size),
                }

    total_size = os.path.getsize(PATH)
    total_chunks = (total_size // CHUNK_SIZE) + 1

    with open(PATH, 'rb') as f:
        for i in range(total_chunks):
            chunk_content = f.read(CHUNK_SIZE)
            encoded_content = base64.b64encode(chunk_content).decode('utf-8')
            chunk_info = {
                "file_info":file_info,
                "total_chunks":str(total_chunks), 
                "chunk_number":str(i),
                "encoded_content":encoded_content
            }
            response = requests.post(REMOTE_URL, data=json.dumps(chunk_info), headers={'Content-Type': 'application/json'})

            if response.status_code != 200:
                print("Erreur lors de l'envoi d'un chunk!")
                return
    print("Envoi terminé avec succès!")

def ask():
    question = input("Entrez votre question : ")
    chat_buffer = ["user : what is your name ?", "system : my name is Sydney"]
    question_info = {
        "user_id" : "1345",
        "question" : question,
        "chat_buffer" : chat_buffer,
    }
    print(question_info)
    response = requests.post(ASK_URL, data=json.dumps(question_info), headers={'Content-Type': 'application/json'}, stream=True)

    # Lisez la réponse ligne par ligne
    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            print(decoded_line, end = "") 
            sys.stdout.flush()

    return

send_chunks()