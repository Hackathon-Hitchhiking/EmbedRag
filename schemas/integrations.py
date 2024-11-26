from pydantic import BaseModel


class PageResponse(BaseModel):
    title: str
    content: bytes | str
