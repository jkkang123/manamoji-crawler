from typing import Optional
from pydantic import BaseModel

class CrawlNewMangaResult(BaseModel):
    resultCode: str
    resultMessage: str
    mangaId: str
