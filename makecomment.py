import praw
import time
from template import TEMPLATE

def make_comment(current_submission, result_set):
    formatted_reply = TEMPLATE.format(result_set['title'],result_set['title_image'],result_set['article'],result_set['images'])
    print(formatted_reply)
    try:
        current_submission.reply(formatted_reply)
    except praw.exceptions.APIException as APIException:
        print(APIException)
        time.sleep(10*60)
        current_submission.reply(formatted_reply)
