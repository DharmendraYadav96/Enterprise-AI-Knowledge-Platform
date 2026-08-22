import os

from pypdf import PdfReader
from docx import Document

from utils.exceptions import ApplicationError


class DocumentLoader:

    def load(self, file_path):

        extension = os.path.splitext(file_path)[1].lower()

        if extension == ".pdf":
            return self._load_pdf(file_path)

        if extension == ".docx":
            return self._load_docx(file_path)

        if extension == ".txt":
            return self._load_txt(file_path)

        raise ApplicationError(
            "Unsupported document format.",
            400
        )

    def _load_pdf(self, file_path):

        try:
            reader = PdfReader(file_path)

            pages = []

            for page in reader.pages:
                text = page.extract_text()

                if text:
                    pages.append(text)

            return "\n".join(pages)

        except Exception as error:
            raise ApplicationError(
                "Failed to extract text from PDF.",
                500
            ) from error

    def _load_docx(self, file_path):

        try:
            document = Document(file_path)

            paragraphs = []

            for paragraph in document.paragraphs:
                if paragraph.text.strip():
                    paragraphs.append(paragraph.text)

            return "\n".join(paragraphs)

        except Exception as error:
            raise ApplicationError(
                "Failed to extract text from DOCX.",
                500
            ) from error

    def _load_txt(self, file_path):

        try:
            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:
                return file.read()

        except Exception as error:
            raise ApplicationError(
                "Failed to read TXT file.",
                500
            ) from error