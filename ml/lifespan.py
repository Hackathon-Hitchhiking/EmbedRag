import torch
import imagebind
from loguru import logger

device = "cuda" if torch.cuda.is_available() else "cpu"

logger.debug("loading imagebind")
imagebind_model = imagebind.model.imagebind_huge(True)
imagebind_model.eval()
imagebind_model.to(device)
