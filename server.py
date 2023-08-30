
import time
import base64
import os
import sys
import json
import asyncio
from fastapi import FastAPI, HTTPException, UploadFile, Form
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

import connectors.mongo_connector as mongo_connector
import connectors.llm_connector as llm_connector
from mytypes import FileInfo, ChunkInfo, Ask_request
from initializer import initialize_vectorbase_table

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mongo_connector.ping_mongodb()

LOCAL = "."
FILE_PATH = LOCAL+'/received_file.pdf'

VECTORBASE_TABLE = initialize_vectorbase_table()
#VECTORBASE_TABLE = {}
print(sys.getsizeof(VECTORBASE_TABLE))
RECEIVED_CHUNKS = {}

@app.post("/upload/")
async def upload(chunk_info: ChunkInfo):
    global RECEIVED_CHUNKS
    encoded_content = chunk_info.encoded_content

    file_info = chunk_info.file_info

    if file_info.title not in RECEIVED_CHUNKS or chunk_info.chunk_number == 0:
        RECEIVED_CHUNKS[file_info.title] = []
        mongo_connector.delete_previous_documents(file_info.user_id)

    RECEIVED_CHUNKS[file_info.title] += [{"encoded_content":encoded_content, "chunk_number":chunk_info.chunk_number}]

    # Check if all chunks are received
    if len(RECEIVED_CHUNKS[file_info.title]) == chunk_info.total_chunks:
        print('all document received')
        create_file(file_info)
        del RECEIVED_CHUNKS[file_info.title]
        return {"status": "received_all_chunks"}
    return {"status": "received_chunk"}    

def create_file(file_info : FileInfo):
    global VECTORBASE_TABLE
    global RECEIVED_CHUNKS

    TEMPFILE_PATH = os.path.join(LOCAL, file_info.title + file_info.type)
    if os.path.exists(TEMPFILE_PATH):
        print(f"Le fichier {TEMPFILE_PATH} existe déjà, il va être supprimé.")
        os.remove(TEMPFILE_PATH)
    else:
        print(f"Le fichier {TEMPFILE_PATH} n'existe pas.")

    sorted_chunks = sorted(RECEIVED_CHUNKS[file_info.title], key=lambda x: int(x['chunk_number']))
    
    with open(TEMPFILE_PATH, 'wb') as f:
        for chunk_info in sorted_chunks:
            encoded_content = chunk_info['encoded_content']
            binary_content = base64.b64decode(encoded_content.encode('utf_8'))
            f.write(binary_content)

    mongo_connector.store_file_in_database(file_info, TEMPFILE_PATH)
    new_vectorbase = llm_connector.create_vectorbase(file_info, TEMPFILE_PATH)
    VECTORBASE_TABLE[file_info.user_id] = new_vectorbase
    return {'message': 'File created'}

@app.post('/ask')
async def ask_endpoint(request: Ask_request):
    question = request.question
    user_id = request.user_id
    chat_buffer = request.chat_buffer
    if user_id not in VECTORBASE_TABLE:
        raise HTTPException(status_code=404, detail="User ID not found in VECTORBASE_TABLE")
    
    vectorbase = VECTORBASE_TABLE[user_id]
    #return StreamingResponse(fake_data_streamer(), media_type='text/event-stream')
    return StreamingResponse(llm_connector.ask_request(question, chat_buffer= chat_buffer, vectorbase=vectorbase), media_type='text/event-stream')