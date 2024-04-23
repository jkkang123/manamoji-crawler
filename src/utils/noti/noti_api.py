import os
from typing import Dict, Optional

import requests

from src.util.constants import NOTI_INFO, Retailer

CRAWL_PRODUCT_NEW_LIST = "crawl_product_new_list"
CRAWL_PRODUCT_PDP = "crawl_product_pdp"
CRAWL_REFRESH_BATCH = "crawl_refresh_batch"
CRAWL_REFRESH_MANUAL = "crawl_refresh_manual"

ENV = os.getenv("env")
common_url = NOTI_INFO[ENV]["url"]
kang_url = NOTI_INFO["kang"]["url"]
kim_url = NOTI_INFO["kim"]["url"]
park_url = NOTI_INFO["park"]["url"]
jung_url = NOTI_INFO["jung"]["url"]
hong_url = NOTI_INFO["hong"]["url"]

# TODO 나중에 enum에 넣어보자
noti_url_dict = {
    Retailer.SEVRES24: kang_url,
    Retailer.GIGLIO: kang_url,
    Retailer.DESILUX: kang_url,
    Retailer.DOUBLEF: kang_url,
    Retailer.LNCC: kim_url,
    Retailer.LUISAVIAROMA: kim_url,
    Retailer.FARFETCH: kim_url,
    Retailer.BROWNSFASHION: kim_url,
    Retailer.MYTHERESA: park_url,
    Retailer.MATCHESFASHION: park_url,
    Retailer.ENDCLOTHING: park_url,
    Retailer.SSENSE: park_url,
    Retailer.HBX: jung_url,
    Retailer.JOMASHOP: jung_url,
    Retailer.FWRD: jung_url,
    Retailer.BABYSHOP: jung_url,
    Retailer.STRANGERPOV: jung_url,
    Retailer.MULBERRY: jung_url,
    Retailer.CATCHFASHION: jung_url,
    Retailer.OUTNET: hong_url,
    Retailer.MRPORTER: hong_url,
    Retailer.NETAPORTER: hong_url,
    Retailer.YOOX: hong_url,
}


def send_noti(
    retailer: Optional[Retailer], job_type: str, cause: str, fields: Optional[Dict] = None, level: str = None
):
    if retailer:
        dict = {"retailer": retailer.value}
    else:
        dict = {}

    if fields:
        dict.update(fields)
    if os.getenv("env") == "local_gcp":
        dict["env"] = "local_gcp 에서 시도했습니다."

    if ENV in ["dev", "local_gcp"]:
        send(common_url, job_type, cause, dict, level)
    elif ENV == "prd":
        if job_type == CRAWL_PRODUCT_NEW_LIST:
            send(common_url, job_type, cause, dict, level)
        elif retailer:
            send(noti_url_dict[retailer], job_type, cause, dict, level)
        else:
            send(common_url, job_type, cause, dict, level)


def send(noti_url: str, job_type: str, cause: str, fields: Dict = None, level: str = None):
    if not noti_url:
        return

    if level == "info":
        job_type_word = f"{job_type} info"
    elif level == "error":
        job_type_word = f"`{job_type} ERROR !!!!`"
    else:
        job_type_word = job_type

    payload = {
        "blocks": [
            {"type": "section", "text": {"type": "mrkdwn", "text": f"{job_type_word}"}},
            {"type": "section", "fields": []},
            {"type": "section", "text": {"type": "mrkdwn", "text": f"*Cause:*```{cause}```"}},
            {"type": "divider"},
        ]
    }

    for field_id in fields.keys():
        field_format = {"type": "mrkdwn", "text": f"*{field_id}*\n{fields.get(field_id)}"}
        payload["blocks"][1]["fields"].append(field_format)

    requests.post(noti_url, json=payload)
