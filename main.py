import logging
from fastapi import FastAPI
from asgi_correlation_id import CorrelationIdMiddleware

from src.crawlers.manga_crawler import crawl_new_manga
from src.entities.crawl_manga_result import CrawlNewMangaResult

crawler = FastAPI()
crawler.add_middleware(CorrelationIdMiddleware)
logger = logging.getLogger(__name__)


@crawler.post("/crawl/manga",
              response_model=CrawlNewMangaResult,
              response_model_exclude_unset=True,
              response_model_exclude_none=True
              )
async def crawl_manga_by_url(url: str):
    return crawl_new_manga(
        url=url
    )
