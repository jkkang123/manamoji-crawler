from abc import ABC
from typing import Optional, Dict

from src.utils.noti import noti_api
from src.utils.noti.noti_api import send_noti


class BaseMangaCrawler(ABC):
    def debug(self, msg: str):
        self.logger.debug(msg)


    def info(self, msg):
        self.logger.info(msg)


    def info_noti(self, msg, body: Optional[Dict] = None):
        self.info(msg)
        send_noti(self.retailer, noti_api.CRAWL_PRODUCT_PDP, msg, body, level="info")


    def warn(self, msg):
        self.logger.warning(msg)


    def error(self, msg):
        self.logger.error(msg)


    def error_noti(self, msg, body: Optional[Dict] = None):
        self.error(msg)
        send_noti(self.retailer, noti_api.CRAWL_PRODUCT_PDP, msg, body, level="error")


    def alert(self, body: dict, cause=None):
        self.error(body)
        self.error(cause)
        send_noti(noti_api.CRAWL_PRODUCT_PDP, body, cause)