import datetime
import io
import os

import django
from celery import shared_task
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from loguru import logger

from core import messages
# Setup django to be able to access the settings file
from core.utils.resources import wrap_text_on_image

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
from apps.social.models import TweetModel, TweetSystemModel
from apps.social.utils import AbstractTweepy
from psycopg2 import OperationalError


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
    try:
        system_status = TweetSystemModel.load()
        at_twt = AbstractTweepy()
        tweet = TweetModel.random_tweet.get_random_tweet()
        if tweet is not None:
            fs = FileSystemStorage()

            imagefile = staticfiles_storage.path('assets/img/thestoicphilo_media_template.png')
            fontfile = staticfiles_storage.path('assets/fonts/Garet-Book.ttf')
            image = wrap_text_on_image(imagefile, fontfile, tweet.tweet_text.upper())

            output = io.BytesIO()
            image.save(output, format="PNG")
            output.seek(0)

            filename = fs.save(f"tweets/tweet_{datetime.datetime.today().date()}.png", output)
            full_filename = fs.path(filename)

            twt_bool, twt_response = at_twt.create_image_tweet(status='', media_filename=full_filename)

            if twt_bool:
                tweet.is_tweeted = True
                tweet.has_image = True
                tweet.tweet_image = filename
                tweet.tweet_date = timezone.now()
                tweet.save()

                sucess_message = f'Tweet #: {tweet.id} posted with image'

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
    except FileNotFoundError as FNF:
        logger.error(f'FileNotFoundError Tweet Image Template: {FNF}')
    except OSError as OE:
        logger.error(f'OSError Font File Missing: {OE}')



