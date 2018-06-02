import praw
from CONFIG import *
from getarticle import get_article
from makecomment import make_comment

reddit = praw.Reddit(user_agent="Allkpop_scraper",client_id=OAUTH_CLIENT,client_secret=OAUTH_SECRET,username=USERNAME,password=PASSWORD)
subreddit = reddit.subreddit(SUBREDDIT)
for submission in subreddit.stream.submissions():
    current_submission = reddit.submission(id=submission)
    url = current_submission.url
    if "allkpop" in url:
        result_set = get_article(url)
        make_comment(current_submission,result_set)