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

Dans le dossier connectors, ajouter le ficher *secrets_manager.py*

## Exécution locale

### Exécuter le serveur FastAPI
Pour démarrer le serveur FastAPI, exécutez la commande suivante :

```bash
uvicorn server:app --reload
```

Le serveur sera accessible à l'adresse http://127.0.0.1:8000.

Assurer la bonne connection avec MongoDB => l'adresse IP doit être autorisée à se connecter. 

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

## Test

Lancer le serveur puis executer les deux fonctions de test.py pour vous assurer du bon fonctionnement. Pour cela, renseigner un path local vers un fichier dans la ligne suivante : 

```python
PATH = "test_file" # Remplacer par un fichier test
```

Puis exécuter les fonctions
```bash
python send_chunks()
```

et 
```bash
python ask()
```
