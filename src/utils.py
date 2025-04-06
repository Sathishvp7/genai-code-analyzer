import os
from git import Repo

from src.logger import logging


logger = logging.getLogger("Utils")

def create_dirs(dir_path: str):
    try:
        logger.info("Entering into create_dirs method for creating folders...")
        os.makedirs(dir_path, exist_ok=True)
    except Exception as e:
        raise e

def repo_ingestion(repo_url: str, repo_saved_path: str):
    try :
        logger.info("Entering into repo_ingestion method for clonning the repo from passed URL....")
        create_dirs(repo_saved_path)
        Repo.clone_from(repo_url, to_path=repo_saved_path)
    except Exception as e:
        raise e
    
