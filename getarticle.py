from urllib.request import urlopen, Request
from bs4 import BeautifulSoup, element
from template import WHITESPACE, AKP_DOMAIN


def get_text_wrapper(soup_elem):
    return get_text(soup_elem)[0].replace(u"\xa0", u" ").strip()


def get_text(soup_elem, img_count=0):
    buff = ""
    if isinstance(soup_elem, element.NavigableString):
        buff += soup_elem
    elif isinstance(soup_elem, element.Tag):
        if soup_elem.contents:
            for child in soup_elem.contents:
                child_buff, img_count = get_text(child, img_count)
                buff += child_buff
        elif soup_elem.name == "img":
            try:
                img_url = soup_elem.attrs["src"]
                if img_url[0] == "/":
                    img_url = AKP_DOMAIN + img_url
                img_count += 1
                buff += "\n\n[image_%02d](%s)\n\n" % (img_count, img_url)
            except KeyError:
                pass
        elif soup_elem.name == "br":
            buff += "\n\n"
    return buff, img_count


def get_article(url):
    page = urlopen(Request(url, headers={"User-Agent": "Mozilla"}))
    soup = BeautifulSoup(page, "html.parser")
    title = soup.title.get_text().replace(" | allkpop", "")
    try:
        title_image = soup.find("img", id="article-image").get("src")
    except AttributeError:
        title_image = ""
    # remove SEE ALSO and tags at the bottom before used by the article div
    try:
        soup.find(
            style="font-size:16px!important;font-weight:bold!important;"
        ).decompose()
    except AttributeError:
        pass
    soup.find("div", id="article-headline-tags").decompose()
    article_div = soup.find("div", class_="entry_content")
    article = get_text_wrapper(article_div)
    result_set = {
        "title": title,
        "title_image": title_image,
        "article": article,
    }
    return result_set
