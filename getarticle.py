from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

def get_article(url):
    page = urlopen(Request(url, headers={'User-Agent': 'Mozilla'}))
    soup = BeautifulSoup(page,"html.parser")
    title = soup.title.get_text()
    title_image = soup.find("img",id="article-image").get("src")
    #remove SEE ALSO and tags at the bottom before used by the article div
    soup.find(style="font-size:16px!important;font-weight:bold!important;").decompose()
    soup.find("div",id="article-headline-tags").decompose()
    article_div = soup.find("div",class_="entry_content")
    article = article_div.get_text().strip().replace(u'\xa0', u' ')
    images = [link.get('src') for link in article_div.find_all("img")]
    image_set = ''.join(images)
    result_set = {'title':title,'title_image':title_image,'article':article,'images': image_set}
    return result_set
