from pydantic import BaseModel

class FileInfo(BaseModel):
    user_id: str
    title: str
    type: str
    size: int

class ChunkInfo(BaseModel):
    file_info: FileInfo
    total_chunks: int
    chunk_number: int
    encoded_content : str

class Ask_request(BaseModel):
    question: str
    chat_buffer : str
    user_id : str