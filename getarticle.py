from urllib.request import urlopen, Request
from bs4 import BeautifulSoup, element
from template import WHITESPACE, AKP_DOMAIN

# deprecated
def image_set_format(image_set):
    if len(image_set) == 0:
        return ""
    string = "Images: "
    for i, image in enumerate(image_set):
        if image[0] == "/":
            image = AKP_DOMAIN + image
        string += "[{}]({}) ".format(i+1,image)
    return string

# deprecated
def article_formatting(article):
    string = ""
    previous = ''
    for part in article:
        if (part == '' or part == ' ') and previous == '':
            pass
        elif (part == '' or part == ' ') and previous != '':
            string += WHITESPACE
        else:
            string += part
        previous = part
    return string

def getTextWrapper(soupElem):
    return getText(soupElem)[0].replace(u'\xa0', u' ').strip()

def getText(soupElem, imgCounter=0):
    buff = ""
    if isinstance(soupElem, element.NavigableString):
        buff += soupElem
    elif isinstance(soupElem, element.Tag):
        if soupElem.contents:
            for child in soupElem.contents:
                cBuff, cCount = getText(child, imgCounter)
                buff += cBuff
                imgCounter = cCount
        elif soupElem.name == 'img':
            try:
                imgPath = soupElem.attrs['src']
                if imgPath[0] == '/':
                    imgPath = AKP_DOMAIN + imgPath
                imgCounter += 1
                buff += "\n\n[image_%02d](%s)\n\n" % (imgCounter, imgPath)
            except KeyError:
                pass
        elif soupElem.name == "br":
            buff += "\n\n"
    return buff, imgCounter

def get_article(url):
    page = urlopen(Request(url, headers={'User-Agent': 'Mozilla'}))
    soup = BeautifulSoup(page,"html.parser")
    title = soup.title.get_text().replace(' | allkpop','')
    try:
        title_image = soup.find("img",id="article-image").get("src")
    except AttributeError:
        title_image = ""
    #remove SEE ALSO and tags at the bottom before used by the article div
    try:
        soup.find(style="font-size:16px!important;font-weight:bold!important;").decompose()
    except AttributeError:
        pass
    soup.find("div",id="article-headline-tags").decompose()
    article_div = soup.find("div",class_="entry_content")
    article = getTextWrapper(article_div)
    result_set = {'title':title,'title_image':title_image,'article':article}
    return result_set
