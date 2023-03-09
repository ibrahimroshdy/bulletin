import datetime
import os

import django
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from loguru import logger
from psycopg2 import OperationalError

from core import messages as core_messages
# Setup django to be able to access the settings file
from core.utils.resources import write_on_image

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.social.models import TweetModel, TweetSystemModel, TwitterAccount
from apps.social.abstract import AbstractTweepy, AbstractSlackAPI


@shared_task
def random_auto_image_tweeter_per_account_process(account):
    """random tweet per account"""
    fontpath = 'assets/fonts/Garet-Book.ttf'
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

            # If there is a tweet available in the database
            if tweet is not None:
                text = tweet.tweet_text.upper()
                imagename = f"accounts/{twitter_account.username}/tweets/tweet_{datetime.datetime.today().date()}.png"
                imagepath = twitter_account.tweet_image_template.url[1:]
                filename, full_filename = write_on_image(imagepath=imagepath,
                                                         fontpath=fontpath,
                                                         imagename=imagename, text=text)

                # Create the tweet with the image
                twt_bool, twt_response = at_twt.create_image_tweet(status='', media_filename=full_filename)

                # If the tweet was created successfully
                if twt_bool:
                    # Update the tweet status in the database
                    tweet.is_tweeted = True
                    tweet.has_image = True
                    tweet.tweet_image = filename
                    tweet.tweet_date = timezone.now()
                    tweet.save()

                    # Log the success message
                    sucess_message = f'Tweet #: {tweet.id} posted with image'
                    logger.success(sucess_message)

                    # Update the system status in the database
                    system_status.set_working(message=sucess_message)

                    # Post the success message to Slack
                    asa_slk.post_message(text=twt_response, channel=slk_channel)

                # If there was an error creating the tweet
                else:
                    # Log the error message
                    logger.error(f'{twt_response}')

                    # Update the system status in the database
                    system_status.set_error(message=twt_response)

                    # Post the error message to Slack
                    asa_slk.post_message(text=twt_response)

            # If there are no tweets available in the database
            else:
                # Log the warning message
                logger.warning(core_messages.TWT_NO_TWEETS_AVAIABLE_IN_DB)
                # Update the system status model with a maintenance message
                system_status.set_maintenance(message=core_messages.TWT_NO_TWEETS_AVAIABLE_IN_DB)
                # Post the error message to Slack
                asa_slk.post_message(text=core_messages.TWT_NO_TWEETS_AVAIABLE_IN_DB)
        else:
            asa_slk = AbstractSlackAPI()
            slack_message = f":x: {core_messages.TWT_ACCOUNT_NOT_REGISTERED}: *{account}*"
            asa_slk.post_message(text=slack_message, channel=settings.SLACK_BOT_CHANNEL)
    except OperationalError as OE:
        logger.error(f'OperationalError DB: {OE}')
    except FileNotFoundError as FNF:
        logger.error(f'FileNotFoundError Tweet Image Template: {FNF}')
    except OSError as OE:
        logger.error(f'OSError Font File Missing: {OE}')
