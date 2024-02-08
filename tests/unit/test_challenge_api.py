import unittest
from src.applications.api_server import create_app


class TestChallengeAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()
        self.app.testing = True

    def test_file_creation(self):
        response = self.app.post("/backend/challenge", json={"id": "123", "name": "test"})
        self.assertEqual(response.status_code, 200)
        with open("123/123.json", "r") as f:
            self.assertEqual(f.read(), '{"id": "123", "name": "test"}')

    def tearDown(self):
        pass
