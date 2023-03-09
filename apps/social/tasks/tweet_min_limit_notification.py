import os
import socket

import django
from celery import shared_task
from loguru import logger

from core import messages as core_messages

# Setup django to be able to access the settings file
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.social.models import TweetModel, TwitterAccount
from apps.social.abstract import AbstractSlackAPI


@shared_task
def tweet_min_limit_notification_process(limit=20, channel='bulletin-news'):
    """
    Sends a notification to a Slack channel if the number of unsent tweets in the database is less than or equal to the
    specified limit.

    Args:
        limit (int): The minimum number of unsent tweets in the database before a notification is sent to Slack.
            Default value is 20.
        :param channel:

    """
    slack_api = AbstractSlackAPI()

    twitter_accounts = TwitterAccount.objects.all()

    for twt_account in twitter_accounts:
        # Query the database for the count of unsent tweets (i.e., tweets where is_tweeted is False)
        twt_objects = TweetModel.objects.filter(is_tweeted=False, twitter_account=twt_account).count()

        # If the count of unsent tweets is less than or equal to the specified limit
        if twt_objects <= limit:
            # Send a notification to Slack with the specified message with hostname
            notification_message = f':warning: *{socket.gethostname()}*: {core_messages.SLK_TWT_TWEETS_IN_DB_CLOSE_TO_LIMIT} of account: *{twt_account.username}*'
            slack_api.post_message(text=notification_message, channel=channel)
            # Log sucessfull slack message sent
            logger.success(core_messages.SLACK_LOGGING_POSTED_200)
