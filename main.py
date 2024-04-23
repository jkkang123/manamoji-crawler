import logging
from fastapi import FastAPI
from asgi_correlation_id import CorrelationIdMiddleware

from src.entities.crawl_manga_result import CrawlMangaResult

crawler = FastAPI()
crawler.add_middleware(CorrelationIdMiddleware)
logger = logging.getLogger(__name__)


@crawler.post("/crawl/manga",
              response_model=CrawlMangaResult,
              response_model_exclude_unset=True,
              response_model_exclude_none=True
              )
async def crawl_manga_by_manga_id(manga_id: str):
    return crawl_pdp_product(
        manga_id=manga_id
    )
