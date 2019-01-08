# AKP reddit bot

A bot that scrapes main article from allkpop article submission on Reddit, then post it as a comment on the submission. Features a rudimentary form of persistence of list. Initially only used on /r/kpop

## Requirements

* Python 3.6

* BeautifulSoup 4

* PRAW

* A valid Reddit API credentials

## Installation

* Clone this repo

* Create a Virtualenv

* `pip install -r requirements.txt`

* copy `CONFIG.py.sample` as `CONFIG.py` and fill with necessary details

* create a blank `requirements.txt`

## CONFIG.py contents

* OAuth Secret key (OAUTH_SECRET)

* OAuth Client key (OAUTH_CLIENT)

* Reddit username (USERNAME)

* Reddit password (PASSWORD)

* Subreddits to stream (SUBREDDITS)

* Persistence filename (FILENAME)