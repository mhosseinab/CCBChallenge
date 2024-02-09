from pathlib import Path

from flask import current_app as app

from config import UPLOADS_PATH as DEFAULT_PATH


class FileStorage:
    def __init__(self, path=DEFAULT_PATH, context=app):
        """
        Create a new FileStorage instance.
        Args:
            path: The root path for the file storage
            context: The Flask application context
        """
        self.path = path
        self.app = context

    def get_full_path(self, folder: str, file_name: str) -> Path:
        """
        Get the full path to a file in the folder with the given name.
        Args:
            folder: target folder
            file_name: target file name

        Returns:
            Path: The full path to the file
        """
        return Path(self.path, folder, file_name)

    def save_file(self, folder: str, file_name: str, content: bytes) -> bool:
        """
        Save the content to a file in the folder with the given name.
        Args:
            folder: target folder
            file_name: target file name
            content: file content

        Returns:
            bool: True if the file was saved successfully, False otherwise
        """
        # Create the full path to the file
        full_path = self.get_full_path(folder, file_name)
        try:
            # Ensure the directory exists
            full_path.parent.mkdir(parents=True, exist_ok=True)

            # Write the content to the file
            with open(str(full_path), "wb") as file:
                file.write(content)
            self.app.logger.debug(f"Saved: {full_path}")
            return True
        except Exception as e:
            self.app.logger.error(f"Failed to write to file: {e}")
            return False

    def delete_file(self, folder: str, file_name: str) -> bool:
        """
        Delete the file with the given name in the folder.
        Args:
            folder:  target folder
            file_name: target file name

        Returns:
            bool: True if the file was deleted successfully, False otherwise
        """

        full_path = self.get_full_path(folder, file_name)

        try:
            # Delete the file
            full_path.unlink()
            self.app.logger.debug(f"Deleted: {full_path}")
            return True
        except Exception as e:
            self.app.logger.error(f"Failed to delete file: {e}")
            return False
