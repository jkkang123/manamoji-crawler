from typing import Optional
from pydantic import BaseModel

class CrawlMangaResult(BaseModel):
    resultCode: str
    resultMessage: str
    mangaId: Optional[str] = None
