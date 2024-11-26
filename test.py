import numpy as np

from configs.Qdrant import client
from repositories.documents import DocumentRepository

client = client

repo = DocumentRepository(client)

ls = np.random.rand(100, 100).tolist()

print(repo.get_document(ls[0], 1))
