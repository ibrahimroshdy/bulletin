import random
from enum import Enum

from django.db import models
from model_utils.models import TimeStampedModel


class TweetSystemStatus(Enum):
    WORKING = "working"
    ERROR = "error"
    MAINTENANCE = "maintenance"
    UNKNOWN = "unknown"


class SingletonModel(TimeStampedModel):
    status = models.CharField(
            max_length=20,
            choices=[(tag.name, tag.value) for tag in TweetSystemStatus]
    )
    message = models.CharField(
            max_length=20,
            null=True
    )

    class Meta:
        # To make it singleton
        abstract = True

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj



class TweetManager(models.Manager):
    def get_random_tweet(self):
        items = list(super(TweetManager, self).filter(is_tweeted=False)[:10])
        if len(items) != 0:
            return random.choice(items)
        else:
            return None

