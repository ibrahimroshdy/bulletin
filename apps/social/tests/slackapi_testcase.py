import os

import django
from django.conf import settings
from django.test import TestCase

from core import messages as core_messages

# Setup django to be able to access the settings file

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.social.abstract import AbstractSlackAPI
from apps.social.tasks import tweet_min_limit_notification_process
from apps.social.models import TwitterAccount


class SlackAPITestCase(TestCase):
    def setUp(self):
        self.slack_sdk_ok = AbstractSlackAPI(token=settings.SLACK_BOT_TOKEN)
        self.slack_sdk_fail = AbstractSlackAPI(token='WRONG_SLACKAPI_TOKEN')
        self.slack_channel = "bulletin-tests"

        self.twitter_account = TwitterAccount.objects.create(username='test',
                                                             twt_bearer_token=settings.TWT_BEARER_TOKEN,
                                                             twt_access_key=settings.TWT_ACCESS_KEY,
                                                             twt_access_secret=settings.TWT_ACCESS_SECRET,
                                                             twt_consumer_key=settings.TWT_CONSUMER_KEY,
                                                             twt_consumer_secret=settings.TWT_CONSUMER_SECRET)

    def test_post_message_sucess(self):
        slack_bool = self.slack_sdk_ok.post_message(text=core_messages.SLACK_MESSAGE_DURING_TESTS_200,
                                                    channel=self.slack_channel)
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
        tweet_min_limit_notification_process(channel=self.slack_channel)

    def tearDown(self):
        TwitterAccount.objects.all().delete()
