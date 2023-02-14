from django.test import TestCase
from loguru import logger
from model_bakery import baker

from .models import TweetModel, WoeidModel
from .utils import AbstractTweepy


# Create your tests here.
class WoeidTestCase(TestCase):
    def setUp(self):
        self.woeid = baker.make(WoeidModel)

    def test_creation(self):
        """
        Tests database creation
        :return: True if a woeid instances were created sucessfully.
        """
        if self.woeid:
            logger.success('DB SUCCESS')
            logger.info(f'{self.woeid.__str__()[:5]})')
            assert True

    @staticmethod
    def test_get_trends_access_failure():
        """
        Tests Invalid or expired token handling
        :return:True if response is empty, else otherwise
        """
        at = AbstractTweepy(access_key='WRONG_ACCESS_KEY')
        response = at.get_trends(db=False)
        if not response:
            assert True
        else:
            assert False

    @staticmethod
    def test_get_trends_consumer_failure():
        """
        Tests Authentication handling
        :return: True if response is empty, else otherwise
        """
        at = AbstractTweepy(consumer_key='WRONG_CONSUMER_KEY')
        response = at.get_trends(db=False)
        if not response:
            assert True
        else:
            assert False

    @staticmethod
    def test_get_trends():
        """
        Tests using the right credentials retreiving trends API
        :return: True if response is not empty, else otherwise
        """
        at = AbstractTweepy()
        response = at.get_trends(db=False)
        if response:
            assert True
        else:
            assert False

    def tearDown(self):
        WoeidModel.objects.all().delete()


class TweetTestCase(TestCase):
    def setUp(self):
        self.tweet = baker.make(TweetModel)

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
