from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate

SYSTEM_TEMPLATE = PromptTemplate.from_template("""
You are an assistant helping the user to find information in a document.
You are given the following pieces of the documents to answer the question at the end.
This pieces are part of a bigger document. They must in in a different order than in the original document.
Give an answer as detailed as possible. 
You must answer very politely and in a way that is easy to understand.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
If the answer has nothing to do with the question, answer that you can only answer questions about the document.
""")

QUESTION_TEMPLATE = PromptTemplate.from_template("""
Here is a extract of the documents your are asked questions about : {context}

Here is the chat history of your conversation with the user : {chat_buffer}

Here is the question of the user: {question}

Based on the documents, answer in the language of the question :
""")