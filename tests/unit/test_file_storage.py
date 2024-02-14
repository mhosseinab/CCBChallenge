import unittest
from unittest import mock
from pathlib import Path
from uuid import uuid4

from src.applications.api_server import create_app
from src.storage.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.client.testing = True
        self.file_storage = FileStorage("uploads", context=self.app)
        pass

    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data=b"test")
    @mock.patch.object(Path, "unlink")
    def test_file_creation(self, mock_unlink, mock_file):
        """
        Test the file creation and deletion functionality of the FileStorage class.
        """
        full_path = self.file_storage.get_full_path("test", "test.txt")
        self.assertEqual(str(full_path), "uploads/test/test.txt")
        self.assertTrue(self.file_storage.save_file("test", "test.txt", b"test"))
        mock_file.assert_called_once_with("uploads/test/test.txt", "wb")
        self.assertTrue(self.file_storage.delete_file("test", "test.txt"))
        mock_unlink.assert_called_once()

    @mock.patch("builtins.open", side_effect=PermissionError())
    def test_file_creation_failure(self, _):
        """
        Test failure scenarios for the file creation functionality of the FileStorage class.
        """
        # Test failure case
        self.assertFalse(self.file_storage.save_file("/root", "test.txt", b"test"))
        self.assertFalse(self.file_storage.delete_file("/root", "test.txt"))

    @mock.patch('pathlib.Path.unlink', side_effect=PermissionError())
    def test_file_delete_failure(self, mock_unlink):
        """
        Test failure scenarios for the file creation functionality of the FileStorage class.
        """
        self.assertFalse(self.file_storage.delete_file("/root", "test.txt"))
        mock_unlink.assert_called_once()

    @mock.patch("builtins.open", side_effect=PermissionError())
    @mock.patch('pathlib.Path.mkdir')
    def test_folder_creation(self, mock_mkdir, _):
        """
        Test the folder creation functionality of the FileStorage class.
        """
        self.file_storage.save_file(str(uuid4()), "test.txt", b"test")
        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)

    @mock.patch('pathlib.Path.mkdir', side_effect=PermissionError())
    def test_folder_creation_failure(self, mock_mkdir):
        """
        Test the folder creation functionality of the FileStorage class.
        """
        self.file_storage.save_file(str(uuid4()), "test.txt", b"test")
        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
