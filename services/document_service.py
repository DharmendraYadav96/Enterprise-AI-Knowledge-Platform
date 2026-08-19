import os
import uuid

from werkzeug.utils import secure_filename

from utils.exceptions import ApplicationError
from utils.logger import setup_logger


class DocumentService:

    ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

    def __init__(self, upload_folder):
        self.upload_folder = upload_folder
        self.logger = setup_logger()

        os.makedirs(self.upload_folder, exist_ok=True)

    def upload_document(self, file):

        if file is None:
            raise ApplicationError("No file was provided.", 400)

        if file.filename == "":
            raise ApplicationError("No file was selected.", 400)

        if not self._is_allowed_file(file.filename):
            raise ApplicationError(
                "Only PDF, DOCX and TXT files are supported.",
                400
            )

        original_filename = secure_filename(file.filename)

        unique_filename = (
            f"{uuid.uuid4().hex}_{original_filename}"
        )

        file_path = os.path.join(
            self.upload_folder,
            unique_filename
        )

        try:
            file.save(file_path)
            self.logger.info("Document uploaded successfully: %s",original_filename)

        except Exception as error:
            self.logger.exception(
                "failed to save document: %s", original_filename
            )
            raise ApplicationError(
                "Failed to save the document.",
                500
            ) from error

        return {
            "original_filename": original_filename,
            "stored_filename": unique_filename,
            "file_path": file_path
        }

    def _is_allowed_file(self, filename):

        if "." not in filename:
            return False

        extension = filename.rsplit(".", 1)[1].lower()

        return extension in self.ALLOWED_EXTENSIONS