from typing import List

from atlassian import confluence

from integrators.base import BaseIntegrator
from schemas.integrations import PageResponse, ResponseType


class ConfluenceIntegration(BaseIntegrator):
    def __init__(self, url: str, username: str, password: str):
        self._conn = confluence.Confluence(
            url=url, username=username, password=password
        )

    def fetch_data(self, page_id: str) -> List[PageResponse]:
        pages = self._conn.get_all_pages_by_label(label=page_id, start=0, limit=100)

        pdfs = []

        for page in pages:
            response = self._conn.get_page_as_pdf(page["id"])

            pdfs.append(PageResponse(title=page["title"], content=response, type=ResponseType.PDF))

        return pdfs

    def close(self):
        self._conn.close()
