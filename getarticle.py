from urllib.request import urlopen, Request
from bs4 import BeautifulSoup, element
from template import WHITESPACE, AKP_DOMAIN

def get_youtube(soup_elem):
    link  = soup_elem.attrs['src'].replace('?','&').replace('embed/', 'watch/?v=')
    title = ""
    try:
        page = urlopen(Request(link, headers={'User-Agent': 'Mozilla'}))
        soup = BeautifulSoup(page,"html.parser")
        title = soup.title.get_text()
        if title == "YouTube":
            title = "Broken Video"
        else:
            title = title.replace(" - YouTube", "")
        title = "YouTube: " + title

    except ValueError:
        pass    # invalid link URL
    return title, link

def get_text_wrapper(soup_elem):
    return get_text(soup_elem).replace(u'\xa0', u' ').strip()

def get_text(soup_elem):
    buff = ""
    if isinstance(soup_elem, element.NavigableString):
        buff += soup_elem
    elif isinstance(soup_elem, element.Tag):
        if soup_elem.name == 'img':
            try:
                imgPath = soup_elem.attrs['src']
                imgName = imgPath[imgPath.rfind('/')+1:imgPath.rfind('.')]

                if imgPath[0] == '/':
                    imgPath = AKP_DOMAIN + imgPath
                buff += "{}[Image: {}]({}){}".format(WHITESPACE, imgName, imgPath, WHITESPACE)
            except KeyError:
                pass
        elif soup_elem.name == 'iframe' and 'src' in soup_elem.attrs:
            title, link = get_youtube(soup_elem)
            if title and link:
                buff += "{}[{}]({}){}".format(WHITESPACE, title, link, WHITESPACE)
        elif soup_elem.contents:
            prefix = ""
            suffix = ""
            if soup_elem.name == 'a':
                try:
                    href = soup_elem.attrs['href']
                    prefix = "["
                    suffix = "]({})".format(href)
                except KeyError:
                    pass
            elif soup_elem.name == 'em':
                prefix = "*"
                suffix = "*"
            elif soup_elem.name == 'strong':
                prefix = "**"
                suffix = "**"
            for child in soup_elem.contents:
                child_buff = get_text(child)
                if not child_buff.isspace():
                    child_buff = prefix + child_buff + suffix
                buff += child_buff
        elif soup_elem.name == "br":
            buff += WHITESPACE
    return buff


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
