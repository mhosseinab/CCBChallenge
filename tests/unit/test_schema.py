import unittest
from pathlib import Path
from unittest import mock

from config import ROOT_PATH
from utils.schema import load_json_data, load_schema

PATH = Path(ROOT_PATH.parent, "tests", "json")


class TestSchema(unittest.TestCase):
    def setUp(self):
        path = str(Path(PATH, "vehicle-features.v1.schema.json"))
        with open(path, 'r') as file:
            self.valid_schema = file.read()
        path = str(Path(PATH, "vehicle-features.v1.json"))
        with open(path, 'r') as file:
            self.valid_json = file.read()
        path = str(Path(PATH, "invalid.json"))
        with open(path, 'r') as file:
            self.invalid_data = file.read()

    def test_load_schema_valid(self):
        with mock.patch("builtins.open", new_callable=mock.mock_open, read_data=self.valid_schema):
            schema = load_schema('vehicle-features.v1.schema.json')
            self.assertIsNotNone(schema)

    def test_load_schema_invalid(self):
        with mock.patch("builtins.open", new_callable=mock.mock_open, read_data=self.invalid_data):
            schema = load_schema('vehicle-features.v1.schema.json')
            self.assertIsNone(schema)

    def test_load_schema_not_found(self):
        with mock.patch("builtins.open", side_effect=FileNotFoundError()):
            schema = load_schema('vehicle-features.v1.schema.json')
            self.assertIsNone(schema)

    def test_load_json_data_valid(self):
        with mock.patch("builtins.open", new_callable=mock.mock_open, read_data=self.valid_json):
            data = load_json_data('vehicle-features.v1.schema.json')
            self.assertIsNotNone(data)

    def test_load_json_data_invalid(self):
        with mock.patch("builtins.open", new_callable=mock.mock_open, read_data=self.invalid_data):
            data = load_json_data('vehicle-features.v1.schema.json')
            self.assertIsNone(data)

    def test_load_json_data_file_not_found(self):
        with mock.patch("builtins.open", side_effect=FileNotFoundError()):
            data = load_json_data('vehicle-features.v1.schema.json')
            self.assertIsNone(data)
