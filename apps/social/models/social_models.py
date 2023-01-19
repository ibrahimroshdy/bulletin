from django.db import models
from model_utils.models import TimeStampedModel

from .helpers import SingletonModel, TweetManager, TweetSystemStatus


# Create your models here.
class WoeidModel(TimeStampedModel):
    id = models.CharField('id', primary_key=True, max_length=90)
    country = models.CharField('country', max_length=256)
    cc = models.CharField('country code', max_length=5)
    active = models.BooleanField('active', default=True)

    def __str__(self):
        return f'{self.cc}.{self.id}'

    class Meta:
        verbose_name = 'Where On Earth ID'
        verbose_name_plural = 'Where On Earth IDs'


class TweetModel(TimeStampedModel):
    tweet_text = models.TextField('tweet_text', max_length=280)
    is_tweeted = models.BooleanField('tweeted', default=False)
    tweet_date = models.DateTimeField('tweeted_date', default=None, null=True)
    # #TODO: add attachment (image)
    # has_attachment = models.BooleanField('tweeted', default=False)

    # Random Tweet field by tweet manager
    random_tweet = TweetManager()

    def __str__(self):
        return f'{self.tweet_date}.{self.is_tweeted}'


class TweetSystemModel(SingletonModel):
    def __str__(self):
        return f'{self.status}'

    def set_error(self):
        self.status = TweetSystemStatus.ERROR.name
        self.save()

    def set_maintenance(self):
        self.status = TweetSystemStatus.MAINTENANCE.name
        self.save()

    def set_working(self):
        self.status = TweetSystemStatus.WORKING.name
        self.save()
    class Meta:
        verbose_name = 'Tweet System Status'
        verbose_name_plural = 'Tweet System Status'
