import os

import django
import tweepy
from django.conf import settings
from loguru import logger

# Setup django to be able to access the settings file
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
from apps.social.models import WoeidModel


class AbstractTweepy:
    """
        An abstract Tweepy class to organize the needed functionalies for Social app
    """

    #TODO: load tokens from enviroment variables
    def __init__(self, consumer_key=settings.TWT_CONSUMER_KEY, consumer_secret=settings.TWT_CONSUMER_SECRET,
                 access_key=settings.TWT_ACCESS_KEY, access_secret=settings.TWT_ACCESS_SECRET):
        try:
            self.auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
            self.auth.set_access_token(access_key, access_secret)
            self.tweepy_api = tweepy.API(self.auth)
        except tweepy.errors.Unauthorized as UNA:
            logger.error(UNA)
        except tweepy.errors.BadRequest as BR:
            logger.error(BR)

    def __get_trends_by_location(self, woeid):
        """
        Get trends to a specific location by where on earth id
        :param woeid: str => where on earth id
        :return: list of trends
        """

        return self.tweepy_api.get_place_trends(woeid)

    @staticmethod
    def __get_woeid_list(db=True):
        """

        :param db: bool: use database or return statically configured params
        :return:
        """
        if db:
            woeid_qs = WoeidModel.objects.filter(active=True).values('id', 'country', 'cc')
            return woeid_qs

        return [
            {
                'id': '23424802',
                'country': 'Egypt',
                'cc': 'EG'
            },

            {
                'id': '1937801',
                'country': 'Saudi Arabia',
                'cc': 'SA'
            }
        ]

    def get_trends(self, db=True):
        """
        An aggration function to utilize private functions in creating a sorted trends object by country name
        :return: a dict object with trends loaded under each country name
        """
        woeid_list = self.__get_woeid_list(db=db)
        response = {}
        try:
            for place in woeid_list:
                response[place['country']] = {
                    'trends': self.__get_trends_by_location(place['id'])[0]['trends'],
                    'cc': place['cc']
                }

            return response
        except tweepy.errors.Unauthorized as UNA:
            logger.error(UNA)
            return response
        except tweepy.errors.BadRequest as BR:
            logger.error(BR)
            return response
