import json
import html
import requests
import pycurl
import certifi
from io import BytesIO
from bs4 import BeautifulSoup

from src.entities.crawl_manga_result import CrawlNewMangaResult
from src.utils.config import get_namu_url


def get_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        return soup
    else:
        return response.status_code

def request_with_pycurl(
        retailer_pdp_api_url,
    ):
    buffer = BytesIO()
    c = pycurl.Curl()

    fake_user_agent = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    )
    c.setopt(pycurl.USERAGENT, fake_user_agent)
    c.setopt(pycurl.URL, retailer_pdp_api_url)
    c.setopt(pycurl.WRITEDATA, buffer)
    c.setopt(pycurl.CAINFO, certifi.where())
    c.perform()
    status_code = c.getinfo(pycurl.RESPONSE_CODE)
    c.close()
    return buffer.getvalue(), status_code


def crawl_new_manga(
    url: str
) -> CrawlNewMangaResult:
    #TODO Return 정의

    # allMangaListHtml = get_html(f'{namuwikiUrl}/w/%EC%9D%BC%EB%B3%B8%20%EB%A7%8C%ED%99%94/%EB%AA%A9%EB%A1%9D')
    #
    # allMangaListTagList = allMangaListHtml.find_all('a')
    # for mangaList in allMangaListTagList:
    #     if '일본 만화/목록/' in mangaList.get_text():
    #         href = mangaList.get('href')
    #         mangaListHtml = get_html(f'{namuwikiUrl + href}')
    #         allMangaTagList = mangaListHtml.find_all('a')
    #         for mangaTag in allMangaTagList:
    #             if mangaTag.get('href') and mangaTag.get('title') and mangaTag.string:
    #                 mangaHtml = get_html(mangaTag.get('href'))
    body, status_code = request_with_pycurl(f'{get_namu_url}/w/%EC%9B%90%20%EC%98%A4%ED%94%84')
    raw = BeautifulSoup(body, "html.parser")
    contents = raw.find_all('script')
    target_json = ''
    for content in contents:
        text = str(content)
        if text.find('window.INITIAL_STATE=') != -1:
            text = text.replace('<script>window.INITIAL_STATE=', '')
            text = text.replace('</script>', '')
            target_json = text
    text_json_1 = json.loads(target_json)

    keys_1 = list(text_json_1.keys())
    text_json_2 = text_json_1[keys_1[2]]

    keys_2 = list(text_json_2.keys())
    text_json_3 = text_json_2[keys_2[2]]

    keys_3 = list(text_json_3.keys())
    text_json_4 = text_json_3[keys_3[6]]

    summary_tag_num = 0
    content_tag_num = 0
    for i in range(1, len(text_json_4)):
        html_string = html.unescape(text_json_4[i])
        content = BeautifulSoup(html_string, 'html.parser')
        summary_tag = content.find(id="개요")
        if summary_tag:
            summary_tag_num = i + 1
        content_tag = content.find(id="줄거리")
        if content_tag:
            content_tag_num = i + 1

    return CrawlNewMangaResult(

    )

