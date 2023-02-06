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
    # TODO: Optimize methods and function calling
    """
    This function performs a process to tweet a randomly selected tweet using the Twitter API.

    Summary:
    The function creates an instance of the `AbstractTweepy` class, which has access to the Twitter API using
    the API keys. It then selects a random tweet from the database using the `get_random_tweet` function of
    `TweetModel`. If a tweet is found, the function tweets it and updates the tweet's information in the database.
    If the tweet posting is unsuccessful, an error message is logged. If no tweets are found in the database,
    a warning message is logged.

    Process:
    1. Load the `TweetSystemModel` to get the system status.
    2. Create an instance of the `AbstractTweepy` class.
    3. Select a random tweet from the database using the `get_random_tweet` function of `TweetModel`.
    4. If a tweet is found:
        a. Tweet the text of the tweet using the `create_tweet` function of the `AbstractTweepy` instance.
        b. If the tweet posting is successful, update the tweet's information in the database.
           Log a success message.
        c. If the tweet posting is unsuccessful, log an error message and update the system status.
    5. If no tweets are found in the database, log a warning message and update the system status.

    Raises:
    OperationalError: If there is an error in the database.
    """
    try:
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
            logger.warning(messages.__NO_TWEETS_AVAIABLE_IN_DB)
            system_status.set_maintenance(message=messages.__NO_TWEETS_AVAIABLE_IN_DB)
    except OperationalError as OE:
        logger.error(f'OperationalError DB: {OE}')
