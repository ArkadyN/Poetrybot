#https://www.reddit.com/r/redditdev/comments/3lotxj/tutorial_how_to_migrate_your_existing_bots_from/

import praw
from prawoauth2 import PrawOAuth2Server        
from reddit_settings import *


reddit_client = praw.Reddit(user_agent=user_agent)
oauthserver = PrawOAuth2Server(reddit_client, app_key, app_secret, state=user_agent, scopes=scopes)
oauthserver.start()

print(oauthserver.get_access_codes())



