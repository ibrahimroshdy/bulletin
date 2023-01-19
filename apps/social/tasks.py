import os

import django
from celery import shared_task
from django.utils import timezone
from loguru import logger

# Setup django to be able to access the settings file
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.social.models import TweetModel
from apps.social.utils import AbstractTweepy


@shared_task
def auto_tweeter_process():
    """
        A celery task that will be picked up.
        The task creates a tweepy instance which has access using Twitter API keys
        and randomly chooses a tweet from the database using a model manager in TweetModel()
        then tweets it and updates the DB
    """

    at_twt = AbstractTweepy()
    tweet = TweetModel.random_tweet.get_random_tweet()
    if tweet is not None:
        twt_bool, twt_response = at_twt.create_random_tweet(text=tweet.tweet_text)
        if twt_bool:
            tweet.is_tweeted = True
            tweet.tweet_date = timezone.now()
            tweet.save()
            logger.success(f'Tweet #: {tweet.id} posted')
        else:
            logger.error(f'{twt_response}')
    else:
        logger.warning('NO MORE TWEETS AVAILABLE IN DATABASE')
