from json import load as json_load, JSONDecodeError
from typing import Optional
from pathlib import Path
from logging import getLogger

from config import SCHEMA_PATH

logger = getLogger(__name__)


def load_schema(schema_name: str) -> Optional[dict]:
    """
    Load a JSON schema from a file
    Args:
        schema_name: the path to the schema file

    Returns:
        dict: The schema as a dictionary
    """
    _path = SCHEMA_PATH / Path(schema_name)
    try:
        with open(_path, "r") as file:
            schema = json_load(file)
        return schema
    except JSONDecodeError:
        logger.error(f"Failed to load schema from {_path}. Invalid JSON format.")
        return None
    except FileNotFoundError:
        logger.error(f"Failed to load schema from {_path}. File not found.")
        return None


def load_json_data(json_file_path: str) -> Optional[dict]:
    try:
        with open(json_file_path, "r") as file:
            data = json_load(file)
        return data
    except JSONDecodeError:
        logger.error(f"Failed to load JSON data from {json_file_path}. Invalid JSON format.")
        return None
    except FileNotFoundError:
        logger.error(f"Failed to load JSON data from {json_file_path}. File not found.")
        return None
