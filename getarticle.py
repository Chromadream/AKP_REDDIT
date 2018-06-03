from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from template import WHITESPACE

def image_set_format(image_set):
    string = ""
    for i in range(len(image_set)):
        string += "[{}]({}) ".format(i+1,image_set[i])
    return string

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

def get_article(url):
    page = urlopen(Request(url, headers={'User-Agent': 'Mozilla'}))
    soup = BeautifulSoup(page,"html.parser")
    title = soup.title.get_text()
    try:
        title_image = soup.find("img",id="article-image").get("src")
    except AttributeError:
        title_image = ""
    #remove SEE ALSO and tags at the bottom before used by the article div
    soup.find(style="font-size:16px!important;font-weight:bold!important;").decompose()
    soup.find("div",id="article-headline-tags").decompose()
    article_div = soup.find("div",class_="entry_content")
    article_div_div = article_div.find_all("div",recursive=False)
    text = [div.get_text().replace(u'\xa0', u' ').strip() for div in article_div_div][:-1]
    images = [link.get('src') for link in article_div.find_all("img")]
    for div in article_div_div:
        div.decompose() #this is disgusting, but so is web scraping
    first_line = soup.find("div",class_="entry_content").get_text().strip()
    article = article_formatting([first_line.replace(u'\xa0', u' ')] + text)
    image_set = image_set_format(images)
    result_set = {'title':title,'title_image':title_image,'article':article,'images': image_set}
    return result_set

print(get_article("https://www.allkpop.com/article/2018/05/kang-daniel-shocks-by-revealing-he-enjoys-eating-raw-bacon"))
