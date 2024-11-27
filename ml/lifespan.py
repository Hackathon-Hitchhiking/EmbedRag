import torch
import imagebind
from loguru import logger
from llm import LLama3Quantized
from config import ModelKwargs
from constants import LLM_PATH

device = "cuda" if torch.cuda.is_available() else "cpu"

logger.debug("loading imagebind")
imagebind_model = imagebind.model.imagebind_huge(True)
imagebind_model.eval()
imagebind_model.to(device)


llm = LLama3Quantized()


kwargs = ModelKwargs(
    temperature=0.7,
    top_k=30,
    top_p=0.9,
    max_tokens=8192,
    repeat_penalty=1.1,
)

llm.load_model(kwargs, LLM_PATH)