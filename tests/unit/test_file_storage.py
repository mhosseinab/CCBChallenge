import unittest
from src.applications.api_server import create_app
from src.storage.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.client.testing = True
        self.file_storage = FileStorage("uploads", context=self.app)
        pass

    def test_file_creation(self):
        """
        Test the file creation and deletion functionality of the FileStorage class.
        """
        full_path = self.file_storage.get_full_path("test", "test.txt")
        self.assertEqual(str(full_path), "uploads/test/test.txt")
        self.assertEqual(self.file_storage.save_file("test", "test.txt", b"test"), True)
        self.assertEqual(self.file_storage.delete_file("test", "test.txt"), True)

    def test_file_creation_failure(self):
        """
        Test failure scenarios for the file creation functionality of the FileStorage class.
        """
        # Test failure case
        self.assertEqual(self.file_storage.save_file("../../../../../root", "test.txt", b"test"), False)
        self.assertEqual(self.file_storage.delete_file("../../../../../root", "test.txt"), False)
