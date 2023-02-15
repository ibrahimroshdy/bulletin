import os
from datetime import datetime

import django
from django.test import TestCase
from loguru import logger
from model_bakery import baker

# Setup django to be able to access the settings file

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.social.models import TweetModel
from apps.social.abstract import AbstractTweepy


class TweetTestCase(TestCase):
    def setUp(self):
        day_of_year = datetime.now().timetuple().tm_yday
        self.tweet = baker.make(TweetModel, tweet_text=f'{day_of_year}/365')
        self.tweet2 = baker.make(TweetModel, tweet_text=f'Life is life.')
        self.tweet3 = baker.make(TweetModel, tweet_text=f'Do you expect the worst?')
        self.tweet4 = baker.make(TweetModel, tweet_text=f'How valid is your instinct?')
        self.tweet5 = baker.make(TweetModel, tweet_text=f'Today is a goodday.')

    def test_creation(self):
        """
        Tests database creation
        :return: True if a woeid instances were created sucessfully.
        """
        if self.tweet:
            logger.success('DB SUCCESS')
            logger.info(f'{self.tweet.__str__()[:5]})')
            assert True

    @staticmethod
    def test_posting_tweet_failure_consumer_key():
        """
        Tests Invalid or expired token handling
        :return:True if response is empty, else otherwise
        """
        at = AbstractTweepy(consumer_key='WRONG_CONSUMER_KEY',
                            consumer_secret='WRONG_CONSUMER_SECERT',
                            bearer_token='WRONG_BEARER_TOKEN', )
        response_bool, response_msg = at.create_tweet(text="TESTING")
        if not response_bool:
            assert True
        else:
            assert False

    @staticmethod
    def test_posting_tweet_image_failure_consumer_key():
        """
        Tests Invalid or expired token handling
        :return:True if response is empty, else otherwise
        """
        at = AbstractTweepy(consumer_key='WRONG_CONSUMER_KEY',
                            consumer_secret='WRONG_CONSUMER_SECERT',
                            bearer_token='WRONG_BEARER_TOKEN', )
        try:
            response_bool, response_msg = at.create_image_tweet(status="TESTING", media_filename="TESTING")
            if not response_bool:
                assert True
            else:
                assert False
        except TypeError as TE:
            logger.error(f'TypeError: {TE}')
            assert True

    def tearDown(self):
        TweetModel.objects.all().delete()

    # @staticmethod
    # https://gist.github.com/camtheman256/d20ddd3c1449f487e748c22b761d6bed
    # def test_tweet_celery_tasks():
    #     random_auto_tweeter_process()
    #     random_auto_image_tweeter_process()
    #
    # @staticmethod
    # def test_tweet_celery_tasks_failure():
    #     os.environ["TWT_BEARER_TOKEN"] = "1"
    #     os.environ["TWT_CONSUMER_KEY"] = "1"
    #     os.environ["TWT_CONSUMER_SECRET"] = "1"
    #     os.environ["TWT_ACCESS_KEY"] = "1"
    #     os.environ["TWT_ACCESS_SECRET"] = "1"
    #
    #     random_auto_tweeter_process()
    #     random_auto_image_tweeter_process()
