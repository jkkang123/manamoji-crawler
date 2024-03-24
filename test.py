import html
import json
import requests
from bs4 import BeautifulSoup

namuwikiUrl = 'https://namu.wiki'
def get_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        return soup
    else:
        return response.status_code

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

raw = get_html(f'{namuwikiUrl}/w/%EC%9B%90%20%EC%98%A4%ED%94%84')
content = raw.find_all('script')
text = str(content[4])
text = text.replace('<script>window.INITIAL_STATE=', '')
text = text.replace('</script>', '')
print(text)
text_json_1 = json.loads(text)

keys_1 = list(text_json_1.keys())
text_json_2 = text_json_1[keys_1[2]]

keys_2 = list(text_json_2.keys())
text_json_3 = text_json_2[keys_2[2]]

keys_3 = list(text_json_3.keys())
text_json_4 = text_json_3[keys_3[6]]

for i in range(1, len(text_json_4)):
    html_string = html.unescape(text_json_4[i])
    content_text = BeautifulSoup(html_string,'html.parser')
    print(content_text.text)