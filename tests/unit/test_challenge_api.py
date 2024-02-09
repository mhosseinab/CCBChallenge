import unittest
from pathlib import Path
from unittest import mock

from flask import json

from config import ROOT_PATH
from src.applications.api_server import create_app
from src.utils.schema import load_json_data

ENDPOINT = "/backend/challenge"


class TestVehicleFeaturesPost(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_vehicle_features_post(self):
        # Define a sample POST request data
        post_data = load_json_data(str(Path(ROOT_PATH.parent, "tests", "json", "vehicle-features.v1.json")))

        # Send a POST request to the /challenge endpoint
        response = self.client.post(
            ENDPOINT,
            data=json.dumps(post_data),
            content_type="application/json",
        )

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the response data is "OK"
        self.assertEqual(response.data, b"OK")

    def test_vehicle_features_post_invalid_data(self):
        # Define invalid POST request data
        post_data = {"invalid": "data"}

        # Send a POST request to the /challenge endpoint
        response = self.client.post(
            ENDPOINT,
            data=json.dumps(post_data),
            content_type="application/json",
        )

        # Assert that the response status code is 400 (Bad Request)
        self.assertEqual(response.status_code, 400)

    def test_vehicle_features_post_save_failure(self):
        # Define a sample POST request data
        post_data = load_json_data(str(Path(ROOT_PATH.parent, "tests", "json", "vehicle-features.v1.json")))

        # Mock the save_file method to always return False
        with mock.patch("storage.file_storage.FileStorage.save_file", return_value=False):
            # Send a POST request to the /challenge endpoint
            response = self.client.post(
                ENDPOINT,
                data=json.dumps(post_data),
                content_type="application/json",
            )

            # Assert that the response status code is 500 (Internal Server Error)
            self.assertEqual(response.status_code, 500)
