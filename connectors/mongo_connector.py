
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from .secrets_manager import MONGO_SECRETS

MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")

URI = "mongodb+srv://pierredelagrandrive:"+MONGO_PASSWORD+"@cluster0.bqzgjh7.mongodb.net/?retryWrites=true&w=majority"
CLIENT = MongoClient(URI, server_api=ServerApi('1'))
DB = CLIENT.pdfcollection
documents_collection = DB.documents
chunks_collection = DB.chunks

try:
    print("Trying to ping MongoDB")
    CLIENT.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

def get_all_items(collection_name : str):
    if collection_name == "documents":
        collection = documents_collection
    return collection.find()

def get_items_in_collection_with_query(collection_name : str, query : dict):
    if collection_name == "chunks":
        collection = chunks_collection
    elif collection_name == "documents":
        collection = documents_collection
    collection.find(query)


def store_file_in_database(file_info, tempfile):
    print("MongoDB - Storing file in database")
    with open(tempfile, 'rb') as f:
        encoded_file = f.read()
        document_data = {
            "user_id": file_info.user_id,
            "title": file_info.title,
            "type": file_info.type,
            "size":file_info.size,  # Vous pouvez remplacer ceci par un titre approprié
            "content": encoded_file
        }
    documents_collection.insert_one(document_data)
    print("MongoDB - File stored in database")
    return

def store_chunks_in_database(file_info, document_chunks):
    chunks_collection.insert_one({"user_id": file_info.user_id, "title": file_info.title, "document_chunks": document_chunks})
    return

def delete_previous_documents(user_id):
    print('MongoDB - deleting previous document for user : '+user_id)
    query = {"user_id": user_id}
    result = documents_collection.delete_many(query)
    print("MongoDB - document deleted")