import praw
from CONFIG import *
from getarticle import get_article
from persistence import *
from makecomment import make_comment

def main():
    reddit = praw.Reddit(user_agent="Allkpop_scraper",client_id=OAUTH_CLIENT,client_secret=OAUTH_SECRET,username=USERNAME,password=PASSWORD)
    subreddit = reddit.subreddit(SUBREDDIT)
    urls = list_urls(FILENAME)
    for submission in subreddit.stream.submissions():
        current_submission = reddit.submission(id=submission)
        url = current_submission.url
        current_url = "{}:{}".format(current_submission.subreddit,url)
        if current_url not in urls and "allkpop" in url:
            result_set = get_article(url)
            make_comment(current_submission,result_set)
            print("Success? {}".format(current_url))
            urls.append(current_url)
            append_url(FILENAME,current_url)