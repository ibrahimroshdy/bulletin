from django.db import models
from model_utils.models import TimeStampedModel


# Create your models here.
class WoeidModel(TimeStampedModel):
    """
    A model representing a 'Where On Earth ID' (WOEID), which is a unique identifier for a specific location on earth.

    Attributes:
        id (CharField): The primary key for the model, with a max length of 90 characters.
        country (CharField): The name of the country associated with the WOEID, with a max length of 256 characters.
        cc (CharField): The country code associated with the WOEID, with a max length of 5 characters.
        active (BooleanField): A flag indicating if the WOEID is active or inactive, with a default value of True.

    Methods:
        __str__: Returns a string representation of the WOEID in the format 'cc.id' (e.g. 'US.1234').

    Meta:
        verbose_name: A human-readable name for the model, set to 'Where On Earth ID'.
        verbose_name_plural: A human-readable name for the model in plural form, set to 'Where On Earth IDs'.
    """
    id = models.CharField('ID', primary_key=True, max_length=90)
    country = models.CharField('Country', max_length=256)
    cc = models.CharField('Country Code', max_length=5)
    active = models.BooleanField('Active', default=True)

    def __str__(self):
        return f'{self.cc}.{self.id}'

    class Meta:
        verbose_name = 'Where On Earth ID'
        verbose_name_plural = 'Where On Earth IDs'
