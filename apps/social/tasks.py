import os

import django
from celery import shared_task
from django.utils import timezone
from loguru import logger

# Setup django to be able to access the settings file
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.social.models import TweetModel, TweetSystemModel
from apps.social.utils import AbstractTweepy


@shared_task
def random_auto_tweeter_process():
    """
        A celery task that will be picked up.
        The task creates a tweepy instance which has access using Twitter API keys
        and randomly chooses a tweet from the database using a model manager in TweetModel()
        then tweets it and updates the DB
    """
    system_status = TweetSystemModel.load()

    at_twt = AbstractTweepy()
    tweet = TweetModel.random_tweet.get_random_tweet()

    if tweet is not None:
        twt_bool, twt_response = at_twt.create_tweet(text=tweet.tweet_text)

        if twt_bool:
            tweet.is_tweeted = True
            tweet.tweet_date = timezone.now()
            tweet.save()

            sucess_message = f'Tweet #: {tweet.id} posted'

            logger.success(sucess_message)
            system_status.set_working(message=sucess_message)
        else:
            logger.error(f'{twt_response}')
            system_status.set_error(message=twt_response)

    else:
        logger.warning('NO MORE TWEETS AVAILABLE IN DATABASE')
        system_status.set_maintenance(message='NO MORE TWEETS AVAILABLE IN DATABASE')


if __name__ == '__main__':
    random_auto_tweeter_process()
