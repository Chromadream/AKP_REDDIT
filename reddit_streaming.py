import praw
from CONFIG import *
from getarticle import get_article
from persistence import *
from makecomment import make_comment
import time


def main():
    reddit = praw.Reddit(
        user_agent="Allkpop_scraper",
        client_id=OAUTH_CLIENT,
        client_secret=OAUTH_SECRET,
        username=USERNAME,
        password=PASSWORD,
    )
    subreddit = reddit.subreddit("kpop")
    urls = list_urls(FILENAME)
    instance_start = time.time()
    for submission in subreddit.stream.submissions():
        url = submission.url
        if submission.domain is not "allkpop.com":
            pass
        entry = "{}:{}".format(submission.subreddit, url)
        if entry not in urls and submission.created_utc > instance_start:
            result_set = get_article(url)
            make_comment(submission, result_set)
            urls.append(entry)
            append_url(FILENAME, entry)
