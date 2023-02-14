import os

import django
from django.conf import settings
from loguru import logger
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError, SlackClientError
from core import messages as core_messages

# Setup django to be able to access the settings file
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()




class AbstractSlackAPI:
    """
        An abstract Slack class to organize the needed functionalies for Social app
    """

    def __init__(self, token=settings.SLACK_BOT_TOKEN):
        try:
            self.client = WebClient(token=token)
        except SlackClientError as SCE:
            logger.error(SCE)

    def post_message(self, text, channel=settings.SLACK_BOT_CHANNEL):
        """
        Post a message to a specified channel in a slack workspace.

        Args:
        - self (object): The instance of the object the method is being called on.
        - text (str): The text to be posted as the message.
        - channel (str, optional): The channel the message should be posted to.
           Defaults to the channel specified in the `settings` module.

        Returns:
        None

        Raises:
        SlackApiError: If there is an error posting the message to the specified channel.

        Logs:
        success: If the message is successfully posted to the channel.
        error: If there is an error posting the message to the channel.
        """
        try:
            response = self.client.chat_postMessage(text=text, channel=channel)
            assert response["message"]["text"] == text
            logger.success(f'{core_messages.SLACK_MESSAGE_POSTED_200}')
        except SlackApiError as SAE:
            # You will get a SlackApiError if "ok" is False
            assert SAE.response["ok"] is False
            assert SAE.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            logger.error(SAE)
