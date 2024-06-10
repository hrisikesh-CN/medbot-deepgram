import logging
import os
from datetime import datetime

from src.constant import ARTIFACT_DIR, LOG_DIR


def get_logger(name: str):
    LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

    logs_path = os.path.join(os.getcwd(),
                             ARTIFACT_DIR,
                             LOG_DIR)

    os.makedirs(logs_path, exist_ok=True)

    LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

    logging.basicConfig(
        filename=LOG_FILE_PATH,
        format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
        level=logging.DEBUG,
    )

    return logging.getLogger(name)
