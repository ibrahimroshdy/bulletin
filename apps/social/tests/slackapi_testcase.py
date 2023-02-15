import os

import django
from django.conf import settings
from django.test import TestCase
from model_bakery import baker

from core import messages as core_messages

# Setup django to be able to access the settings file

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.social.abstract import AbstractSlackAPI
from apps.social.models import TweetModel
from apps.social.tasks import tweet_min_limit_notification_process


class SlackAPITestCase(TestCase):
    def setUp(self):
        self.slack_sdk_ok = AbstractSlackAPI(token=settings.SLACK_BOT_TOKEN)
        self.slack_sdk_fail = AbstractSlackAPI(token='WRONG_SLACKAPI_TOKEN')
        self.tweet2 = baker.make(TweetModel, tweet_text=f'Life is life.')
        self.tweet3 = baker.make(TweetModel, tweet_text=f'Do you expect the worst?')
        self.tweet4 = baker.make(TweetModel, tweet_text=f'How valid is your instinct?')
        self.tweet5 = baker.make(TweetModel, tweet_text=f'Today is a goodday.')

    def test_post_message_sucess(self):
        slack_bool = self.slack_sdk_ok.post_message(text=core_messages.SLACK_MESSAGE_DURING_TESTS_200)
        if slack_bool:
            assert True
        else:
            assert False

    def test_post_message_failure(self):
        slack_bool = self.slack_sdk_fail.post_message(text="THIS MESSAGE SHOULDN'T BE SENT")
        if not slack_bool:
            assert True
        else:
            assert False

    def test_tweet_count_notification(self):
        tweet_min_limit_notification_process()
