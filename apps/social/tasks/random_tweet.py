import os

import django
from celery import shared_task
from django.utils import timezone
from loguru import logger

from psycopg2 import OperationalError

# Setup django to be able to access the settings file

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.social.models import TweetModel, TweetSystemModel
from apps.social.abstract import AbstractTweepy, AbstractSlackAPI
from core import messages as core_messages


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
    # Load the system status model
    try:
        system_status = TweetSystemModel.load()
        # Create an instance of the AbstractTweepy class
        at_twt = AbstractTweepy()
        # Get a random tweet from the TweetModel
        tweet = TweetModel.random_tweet.get_random_tweet()
        # Create an instance of the AbstractSlackAPI class
        asa_slk = AbstractSlackAPI()

        # If a tweet is retrieved
        if tweet is not None:
            # Call the create_tweet method of the AbstractTweepy class
            twt_bool, twt_response = at_twt.create_tweet(text=tweet.tweet_text)

            # If the tweet is successfully posted
            if twt_bool:
                # Update the tweet in the database
                tweet.is_tweeted = True
                tweet.tweet_date = timezone.now()
                tweet.save()

                # Prepare a success message
                sucess_message = f'Tweet #: {tweet.id} posted'

                # Log the success message
                logger.success(sucess_message)

                # Update the system status model
                system_status.set_working(message=sucess_message)

                # Post the success message to Slack
                asa_slk.post_message(text=sucess_message)
            else:
                # Log the error message
                logger.error(f'{twt_response}')
                # Update the system status model with the error message
                system_status.set_error(message=twt_response)

                # Post the error message to Slack
                asa_slk.post_message(text=twt_response)

        # If no tweet is retrieved
        else:
            # Log a warning message
            logger.warning(core_messages.TWT_NO_TWEETS_AVAIABLE_IN_DB)
            # Update the system status model with a maintenance message
            system_status.set_maintenance(message=core_messages.TWT_NO_TWEETS_AVAIABLE_IN_DB)
            # Post the error message to Slack
            asa_slk.post_message(text=core_messages.TWT_NO_TWEETS_AVAIABLE_IN_DB)

    # Handle the operational error
    except OperationalError as OE:
        # Log the operational error
        logger.error(f'OperationalError DB: {OE}')
