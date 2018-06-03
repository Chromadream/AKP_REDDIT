import praw
import time
from template import TEMPLATE

def formatting(result_set):
    return TEMPLATE.format(result_set['title'],result_set['title_image'],result_set['article'],result_set['images'])

def make_comment(current_submission, result_set):
    formatted_reply = formatting(result_set)
    try:
        current_submission.reply(formatted_reply)
    except praw.exceptions.APIException:
        time.sleep(10*60)
        current_submission.reply(formatted_reply)
