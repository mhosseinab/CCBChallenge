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
        """
        Test the file creation functionality of the FileStorage class.
        This includes testing both successful file creation and failure scenarios.
        """
        file_storage = FileStorage("uploads", context=self.app)
        full_path = file_storage.get_full_path("test", "test.txt")
        self.assertEqual(str(full_path), "uploads/test/test.txt")
        self.assertEqual(file_storage.save_file("test", "test.txt", b"test"), True)

        # Test failure case
        self.assertEqual(file_storage.save_file("../../../../../root", "test.txt", b"test"), False)
        self.assertEqual(file_storage.delete_file("../../../../../root", "test.txt"), False)

        self.assertEqual(file_storage.delete_file("test", "test.txt"), True)
