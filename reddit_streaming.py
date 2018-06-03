import praw
from CONFIG import *
from getarticle import get_article
from persistence import *
from makecomment import make_comment
import time

def fetch_new_URLs(domain_instance):
    return domain_instance.new()

def main():
    reddit = praw.Reddit(user_agent="Allkpop_scraper",client_id=OAUTH_CLIENT,client_secret=OAUTH_SECRET,username=USERNAME,password=PASSWORD)
    domain = reddit.domain('allkpop.com')
    urls = list_urls(FILENAME)
    instance_start = time.time()
    while True:
        dataset = fetch_new_URLs(domain)
        for submission in dataset:
            current_submission = reddit.submission(id=submission)
            url = current_submission.url
            current_url = "{}:{}".format(current_submission.subreddit,url)
            if current_url not in urls and current_submission.created_utc > instance_start:
                result_set = get_article(url)
                make_comment(current_submission,result_set)
                print("Success? {}".format(current_url))
                urls.append(current_url)
                append_url(FILENAME,current_url)
