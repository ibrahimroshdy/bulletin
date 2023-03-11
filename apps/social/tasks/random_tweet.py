import os

import django
from celery import shared_task
# Setup django to be able to access the settings file
from django.conf import settings
from django.utils import timezone
from loguru import logger
from psycopg2 import OperationalError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.social.models import TweetModel, TweetSystemModel, TwitterAccount
from apps.social.abstract import AbstractTweepy, AbstractSlackAPI
from core import messages as core_messages


@shared_task
def random_auto_tweeter_per_account_process(account):
    """process tweeting a random tweet per account"""
    # Load the system status model
    try:
        # Get twitter account data
        is_twt_account_in_db = TwitterAccount.objects.filter(username=account).exists()

        if is_twt_account_in_db:
            twitter_account = TwitterAccount.objects.get(username=account)
            # Get a random tweet from the TweetModel
            tweet = TweetModel.random_tweet.get_random_tweet(twitter_account=account)
            # Create an instance of the AbstractTweepy class
            at_twt = AbstractTweepy(consumer_key=twitter_account.twt_consumer_key,
                                    consumer_secret=twitter_account.twt_consumer_secret,
                                    access_key=twitter_account.twt_access_key,
                                    access_secret=twitter_account.twt_access_secret,
                                    bearer_token=twitter_account.twt_bearer_token)

            # Create an instance of the AbstractSlackAPI class
            asa_slk = AbstractSlackAPI(token=twitter_account.slk_bot_token)
            slk_channel = twitter_account.slk_bot_channel

            system_status = TweetSystemModel.load()

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
                    sucess_message = f":white_check_mark: Tweet #: {tweet.id} posted"

                    # Log the success message
                    logger.success(sucess_message)

                    # Update the system status model
                    system_status.set_working(message=sucess_message)

                    # Post the success message to Slack
                    asa_slk.post_message(text=sucess_message, channel=slk_channel)
                else:
                    # Log the error message
                    logger.error(f'{twt_response}')

                    # Update the system status model with the error message
                    system_status.set_error(message=twt_response)

                    # Post the error message to Slack
                    asa_slk.post_message(text=twt_response, channel=slk_channel)

            # If no tweet is retrieved
            else:
                # Log a warning message
                logger.warning(core_messages.TWT_NO_TWEETS_AVAIABLE_IN_DB)
                # Update the system status model with a maintenance message
                system_status.set_maintenance(message=core_messages.TWT_NO_TWEETS_AVAIABLE_IN_DB)
                # Post the error message to Slack
                asa_slk.post_message(text=core_messages.TWT_NO_TWEETS_AVAIABLE_IN_DB, channel=slk_channel)
        else:
            asa_slk = AbstractSlackAPI()
            slack_message = f":x: {core_messages.TWT_ACCOUNT_NOT_REGISTERED}: *{account}*"
            asa_slk.post_message(text=slack_message, channel=settings.SLACK_BOT_CHANNEL)

    # Handle the operational error
    except OperationalError as OE:
        # Log the operational error
        logger.error(f'OperationalError DB: {OE}')
