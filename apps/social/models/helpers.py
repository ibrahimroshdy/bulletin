import random
from enum import Enum

from django.db import models
from model_utils.models import TimeStampedModel


class TweetSystemStatus(Enum):
    """
    Enum class to maintain tag and value of tweet status
    """
    WORKING = "working"
    ERROR = "error"
    MAINTENANCE = "maintenance"
    UNKNOWN = "unknown"


class SingletonModel(TimeStampedModel):
    """
    A singleton Django Model to havee only one row in the database.
    Used by the .load() function
    """
    status = models.CharField(
            max_length=20,
            choices=[(tag.name, tag.value) for tag in TweetSystemStatus],
            default=TweetSystemStatus.UNKNOWN.name
    )
    message = models.TextField(
            max_length=1000,
            null=True
    )

    class Meta:
        # To make it singleton
        abstract = True

    @classmethod
    def load(cls):
        """
        A load fucntion to ensure the existance of one object
        :return: A single object of the singleton model with pk=1
        """
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class TweetManager(models.Manager):
    """
    A tweet manager model to add custom made functions
    """

    def get_random_tweet(self):
        """
        A method to filter through a model with given filters and get the last ten items
        :return: A random choice of the list of 10 items
        """
        items = list(super(TweetManager, self).filter(is_tweeted=False)[:10])
        if len(items) != 0:
            return random.choice(items)
        else:
            return None
