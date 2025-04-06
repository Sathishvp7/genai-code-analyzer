from dotenv import load_dotenv
import os

from langchain.vectorstores import Chroma

from src import helper
from src import constants
from src.exception import CustomException
from src.logger import logging

logger = logging.getLogger("Store_Index")
load_dotenv()

documents = helper.load_repo(constants.SCAN_REPO_PATH)
text_chunks = helper.document_splitter(document=documents)
embedding_model = helper.load_embedding_model()

## Setting up the Chroma Vector DB
vectorDB = Chroma.from_documents(
    text_chunks, 
    embedding=embedding_model, 
    persist_directory=constants.VECTOR_DB_DATA_PATH
)
vectorDB.persist()
