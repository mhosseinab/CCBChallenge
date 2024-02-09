from json import load as json_load
from pathlib import Path

from config import SCHEMA_PATH


def load_schema(schema_name: str):
    """
    Load a JSON schema from a file
    Args:
        schema_name: the path to the schema file

    Returns:
        dict: The schema as a dictionary
    """
    _path = SCHEMA_PATH / Path(schema_name)
    with open(_path, 'r') as file:
        schema = json_load(file)
    return schema


def load_json_data(json_file_path: str):
    with open(json_file_path, 'r') as file:
        data = json_load(file)
    return data
