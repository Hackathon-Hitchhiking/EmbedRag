from typing import List

from importers.base import BaseIntegrator
from notion_client import Client

from schemas.integrations import PageResponse


class NotionIntegration(BaseIntegrator):
    def __init__(self, api_token: str):
        self._conn = Client(auth=api_token)

    def fetch_data(self, page_id: str) -> List[PageResponse]:
        page = self._conn.pages.retrieve(page_id)

        # TODO fix this and testing

        contents = []
        page_title = page["properties"]["title"]["title"][0]["plain_text"]

        children = self._conn.blocks.children.list(page_id=page_id).get("results", [])

        for child in children:
            content = ""
            if child["type"] == "child_page":
                sub_page_id = child["id"]
                contents += self.fetch_data(sub_page_id)
            elif child["type"] == "paragraph":
                paragraph_text = "".join(
                    [text["plain_text"] for text in child["paragraph"]["rich_text"]]
                )
                content += f"{paragraph_text}\n\n"

        return contents

    def close(self):
        self._conn.close()
