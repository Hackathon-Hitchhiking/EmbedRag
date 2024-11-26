import tempfile

import torch
from imagebind.model import ModalityType
from imagebind.utils import data

from ml.lifespan import device, imagebind_model


class MlService:
    def __init__(self):
        self._imagebind_model = imagebind_model

        self.device = device

    def _extract_text_embedding(self, text: str) -> torch.Tensor:
        """
        Извлекает эмбеддинг для текста.

        Параметры
        ----------
        text : str
            Входной текст для извлечения эмбеддинга. Если строка пустая или не является строкой,
            будет использовано значение по умолчанию "<UNK>".

        Возвращает
        -------
        torch.Tensor
            Эмбеддинг текста, полученный с помощью модели ImageBind.

        Примечания
        ---------
        Функция использует метод `load_and_transform_text` для предварительной обработки текста,
        приводя его в формат, подходящий для обработки моделью. Затем эмбеддинг извлекается
        в режиме inference, что позволяет выполнять вычисления без сохранения промежуточных
        данных для обучения.

        Исключения
        ---------
        Проверка типа входных данных выполняется с целью обеспечения безопасности и предотвращения
        ошибок при передаче некорректного формата. Если переданный текст не соответствует
        ожидаемому типу, используется placeholder "<UNK>".
        """
        if not isinstance(text, str) or not text:
            text = "<UNK>"
        inputs = {ModalityType.TEXT: data.load_and_transform_text([text], self.device)}
        with torch.inference_mode():
            text_embedding = self._imagebind_model(inputs)[ModalityType.TEXT]
        return text_embedding

    def _extract_image_embeddings(self, image: bytes):
        with tempfile.NamedTemporaryFile(delete=True) as temp:
            temp.write(image)
            inputs = {
                ModalityType.VISION: data.load_and_transform_vision_data(
                    [temp.name], self.device
                )
            }
            with torch.inference_mode():
                vision_embedding = self._imagebind_model(inputs)[ModalityType.TEXT]
            return vision_embedding
