import torch
import base64
from io import BytesIO
from typing import List, Dict, Any
from ml.lifespan import device, imagebind_model
from imagebind.model import ModalityType
from imagebind.utils import data

from repositories.documents import DocumentRepository
from schemas.documnet import CreateDocumentOpts
from ml.utils import DocxProcessor, PdfProcessor


class MlService:
    def __init__(self):
        self._imagebind_model = imagebind_model
        self.device = device
        self.document_repository = DocumentRepository()

    def _extract_text_embedding(self, text: str) -> torch.Tensor:
        """
        Извлекает эмбеддинг для текста.
        """
        if not isinstance(text, str) or not text:
            text = "<UNK>"
        inputs = {ModalityType.TEXT: data.load_and_transform_text([text], self.device)}
        with torch.inference_mode():
            text_embedding = self._imagebind_model(inputs)[ModalityType.TEXT]
        return text_embedding

    def process_and_store_document(self, file_bytes: bytes) -> None:
        """
        Обрабатывает документ, векторизует чанки и сохраняет их в Qdrant.
        :param file_bytes: Содержимое .docx файла в байтах.
        """
        docx_processor = DocxProcessor()
        chunks = list(docx_processor.process(file_bytes))
        documents = []

        for chunk in chunks:
            text = chunk['chunk']
            metadata = chunk['metadata']

            embedding = self._extract_text_embedding(text).squeeze().tolist()

            images_metadata = [
                {
                    "position": img.get("position"),
                }
                for img in metadata.get('images', [])
            ]

            metadata_to_store = {
                "text": text,
                "start_word": metadata.get("start_word"),
                "end_word": metadata.get("end_word"),
                "images": images_metadata,
            }

            document_opt = CreateDocumentOpts(
                vector=embedding,
                metadata=metadata_to_store
            )

            documents.append(document_opt)

        self.document_repository.create_document(documents)
