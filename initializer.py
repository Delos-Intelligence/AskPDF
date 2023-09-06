import os

from mytypes import FileInfo
import connectors.mongo_connector as mongo_connector
import connectors.llm_connector as llm_connector

LOCAL = "."
FILE_PATH = LOCAL+'/received_file.pdf'

VECTORBASE_TABLE = {} 

def initialize_vectorbase_table():
    print("Initializing VECTORBASE_TABLE")
    global VECTORBASE_TABLE
    documents = mongo_connector.get_all_items("documents")
    for document in documents:
        file_info = FileInfo(
            user_id = document['user_id'],
            title = document['title'],
            type = document['type'],
            size = document['size'],
            uuid= document['uuid']
        )
        binary_content = document['content']
        TEMPFILE_PATH = os.path.join(LOCAL, file_info.title + file_info.type)
        with open(TEMPFILE_PATH, 'wb') as f:
            f.write(binary_content)
        vectorbase = llm_connector.create_vectorbase(file_info, TEMPFILE_PATH)
        VECTORBASE_TABLE[file_info.user_id] = vectorbase
    print("VECTORBASE_TABLE initialized")
    return VECTORBASE_TABLE