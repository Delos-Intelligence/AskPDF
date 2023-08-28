# AskPDF

## Installation

### Prérequis
Python 3.8 ou supérieur
MongoDB

### Installer les dépendances
Clonez le dépôt et naviguez dans son répertoire, puis exécutez :

```bash
pip install -r requirements.txt
```

## Exécution locale

### Exécuter le serveur FastAPI
Pour démarrer le serveur FastAPI, exécutez la commande suivante :

```bash
uvicorn server:app --reload
```

Le serveur sera accessible à l'adresse http://127.0.0.1:8000.

## Endpoints
### Upload
Pour envoyer un fichier par morceaux :

```bash
POST /upload/
```

Body 

```json
{
  "file_info": {
    "user_id": "1234",
    "title": "file",
    "type": ".pdf",
    "size": 5000
  },
  "total_chunks": 10,
  "chunk_number": 1,
  "encoded_content": "base64 du morceau de fichier"
}
```

### Ask
Pour demander quelque chose :

```json
{
  "question": "Votre question ici",
  "chat_buffer": "Votre historique de discussion",
  "user_id": "1234"
}
```

