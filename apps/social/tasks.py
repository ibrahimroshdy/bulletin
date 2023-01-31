import os

import django
from celery import shared_task
from django.utils import timezone
from loguru import logger

from core import messages

# Setup django to be able to access the settings file
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.social.models import TweetModel, TweetSystemModel
from apps.social.utils import AbstractTweepy
from psycopg2 import OperationalError


@shared_task
def random_auto_tweeter_process():
    """
        A celery task that will be picked up.
        The task creates a tweepy instance which has access using Twitter API keys
        and randomly chooses a tweet from the database using a model manager in TweetModel()
        then tweets it and updates the DB
    """
    try:
        system_status = TweetSystemModel.objects.get(pk=1)

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
            logger.warning(messages.__NO_TWEETS_AVAIABLE_IN_DB)
            system_status.set_maintenance(message=messages.__NO_TWEETS_AVAIABLE_IN_DB)
    except OperationalError as OE:
        logger.error(f'OperationalError DB: {OE}')

# if __name__ == '__main__':
#     random_auto_tweeter_process()
