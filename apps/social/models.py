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
