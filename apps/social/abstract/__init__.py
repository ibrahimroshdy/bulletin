"""
This module provides abstract base classes for communicating with APIs for Slack and Twitter.

The `AbstractSlackAPI` class from `abstract_slackclient` module is
an abstract base class that provides a basic interface for communicating with the Slack API.

The `AbstractTweepy` class from `abstract_tweepy` module is
an abstract base class that provides a basic interface for communicating with the Twitter API.
"""

from .abstract_slackclient import AbstractSlackAPI
from .abstract_tweepy import AbstractTweepy
