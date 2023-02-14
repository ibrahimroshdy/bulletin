import datetime
import io
import os

import django
from celery import shared_task
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from loguru import logger
from psycopg2 import OperationalError

from core import messages as core_messages
# Setup django to be able to access the settings file
from core.utils.resources import wrap_text_on_image

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.social.models import TweetModel, TweetSystemModel
from apps.social.utils import AbstractTweepy, AbstractSlackAPI


@shared_task
def random_auto_image_tweeter_process():
    # TODO: Optimize methods and function calling
    """
    random_auto_image_tweeter_process

    Summary:
        This function performs the process of tweeting an image with a random tweet text from the database.

    Process:
    1. Loads the system status from the database using`TweetSystemModel.load()
    2. Instantiates the AbstractTweepy object at_twt
    3. Loads a random tweet from the database using TweetModel.random_tweet.get_random_tweet()
    4. If a tweet is found, the text is wrapped on an image using wrap_text_on_image
    5. The image is then saved to the file system using FileSystemStorage and the tweet is updated to reflect that it has been tweeted
    6. The image tweet is then created using at_twt.create_image_tweet
    7. If the image tweet is created successfully, the system status is updated to reflect success and a success message is logged
    8. If the image tweet cannot be created, an error message is logged and the system status is updated to reflect an error
    9. If there are no available tweets in the database, a warning message is logged and the system status is updated to reflect maintenance.

    Raises:
        OperationalError: If an operational error occurs while accessing the database.
    """
    # Load the system status model
    try:
        system_status = TweetSystemModel.load()

        # Initialize the abstract class for Twitter API
        at_twt = AbstractTweepy()

        # Get a random tweet from the database
        tweet = TweetModel.random_tweet.get_random_tweet()

        # Initialize the abstract class for Slack API
        asa_slk = AbstractSlackAPI()

        # If there is a tweet available in the database
        if tweet is not None:
            # Initialize the file system storage
            fs = FileSystemStorage()

            # Get the image file and font file paths
            imagefile = staticfiles_storage.path('assets/img/thestoicphilo_media_template.png')
            fontfile = staticfiles_storage.path('assets/fonts/Garet-Book.ttf')

            # Wrap the tweet text on the image
            image = wrap_text_on_image(imagefile, fontfile, tweet.tweet_text.upper())

            # Create a memory buffer for the output image
            output = io.BytesIO()

            # Save the output image in PNG format to the memory buffer
            image.save(output, format="PNG")

            # Set the file pointer to the beginning of the buffer
            output.seek(0)

            # Save the output image to the file system
            filename = fs.save(f"tweets/tweet_{datetime.datetime.today().date()}.png", output)
            full_filename = fs.path(filename)

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
                asa_slk.post_message(text=sucess_message)

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

    except OperationalError as OE:
        logger.error(f'OperationalError DB: {OE}')
    except FileNotFoundError as FNF:
        logger.error(f'FileNotFoundError Tweet Image Template: {FNF}')
    except OSError as OE:
        logger.error(f'OSError Font File Missing: {OE}')
