import random

from django.db import models
from model_utils.models import TimeStampedModel


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


# #TODO: possibility of making this avaliable
# class TwitterKeysSecretsModel(TimeStampedModel):
#     TWT_CONSUMER_KEY = models.CharField('TWT_CONSUMER_KEY', max_length=256)
#     TWT_CONSUMER_SECRET = models.CharField('TWT_CONSUMER_SECRET', max_length=256)
#     TWT_ACCESS_KEY = models.CharField('TWT_ACCESS_KEY', max_length=256)
#     TWT_ACCESS_SECRET = models.CharField('TWT_ACCESS_KEY', max_length=256)

class TweetManager(models.Manager):
    def get_random_tweet(self):
        items = list(super(TweetManager, self).filter(is_tweeted=False)[:10])
        if len(items) != 0:
            return random.choice(items)
        else:
            return None


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
