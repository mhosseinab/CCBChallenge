import unittest
from src.applications.api_server import create_app
from src.storage.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.client.testing = True
        pass

    def test_file_creation(self):
        file_storage = FileStorage("uploads", context=self.app)
        full_path = file_storage.get_full_path("test", "test.txt")
        self.assertEqual(str(full_path), "uploads/test/test.txt")
        self.assertEqual(file_storage.save_file("test", "test.txt", "test"), True)
        self.assertEqual(file_storage.delete_file("test", "test.txt"), True)
