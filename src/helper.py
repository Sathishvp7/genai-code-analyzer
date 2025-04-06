import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders.generic import GenericLoader
from langchain.text_splitter import Language, RecursiveCharacterTextSplitter
from langchain_community.document_loaders.parsers.language.language_parser import LanguageParser
from langchain_community.vectorstores import Chroma
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.schema.prompt_template import format_document

from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

from src import constants
from src.logger import logging
from src.exception import CustomException
from src import utils

logger = logging.getLogger("Helper")
load_dotenv()

def repo_ingestion(repo_url: str):
    logger.info("Entering into repo_ingestion method............")
    try:
        repo_path = constants.SCAN_REPO_PATH
        utils.repo_ingestion(repo_url, repo_path)
    except Exception as e:
        raise CustomException(e, sys)

def load_repo(repo_path: str):
    logger.info("Entering into load_repo method for code analysis......")
    try:       
        loader = GenericLoader.from_filesystem(
            repo_path, 
            glob="**/*", suffixes=[constants.SUFFIX], 
            parser=LanguageParser(
                language=Language.PYTHON, 
                parser_threshold=500
            )
        )
    except Exception as e:
        logger.exception("Exception from:-> ", e)
        raise CustomException(e, sys)

    return loader.load()

def document_splitter(document): 
    logger.info("Entering into document_splitter method........")
    try:
        document_splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.PYTHON,
            chunk_size = constants.SPLITTER_CHUNK_SIZE,
            chunk_overlap = constants.SPLITTER_CHUNK_OVERLAP
        )
        document_chunks = document_splitter.split_documents(document)
    except Exception as e:
        logger.exception(e, sys)
        raise CustomException(e, sys)
    return document_chunks

    

def load_embedding_model():
    logger.info("Entering into load_embedding_model.......")
    return GoogleGenerativeAIEmbeddings(google_api_key=os.getenv("GEMINI_API_KEY"), model=constants.EMBEDDING_MODEL_NAME)

def get_prompt():
    logger.info("Getting the prompt for LLM model.........")
    try:
        prompt_template = """You are an powerful assistantfor question-answering tasks You have to tell the Usr.
        Use the following context to answer the question.
        If you don't know the answer, just say that you don't know.
        Use five sentences maximum and keep the answer concise.\n
        Question: {question} \nContext: {context} \nAnswer:
        """

        return PromptTemplate.from_template(prompt_template)
    except Exception as e:
        raise CustomException(e, sys)
    
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)