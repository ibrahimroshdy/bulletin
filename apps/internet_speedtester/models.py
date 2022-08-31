from datetime import timedelta

from django.db import models
from django.utils import timezone
from model_utils.models import TimeStampedModel


class ClientModel(TimeStampedModel):
    ip = models.GenericIPAddressField('ipaddress')
    lat = models.FloatField('lat')
    lon = models.FloatField('lon')
    isp = models.CharField('internet service provider', max_length=256)
    cc = models.CharField('country code', max_length=5)

    def __str__(self):
        return f'{self.cc}.{self.isp}'

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'


class ServersModel(TimeStampedModel):
    id = models.IntegerField('id', primary_key=True)
    url = models.URLField('url')
    lat = models.FloatField('lat')
    lon = models.FloatField('lon')
    name = models.CharField('city', max_length=256)
    country = models.CharField('country', max_length=256)
    cc = models.CharField('country code', max_length=5)
    sponsor = models.CharField('sponsor', max_length=256)
    host = models.CharField('host', max_length=256)
    d = models.FloatField('d')
    latency = models.FloatField('latency', null=True, blank=True)

    def __str__(self):
        return f'{self.cc}.{self.name}'

    class Meta:
        verbose_name = 'Server'
        verbose_name_plural = 'Servers'


class SpeedtesterModel(TimeStampedModel):
    best_server = models.ForeignKey(ServersModel, on_delete=models.CASCADE)
    client = models.ForeignKey(ClientModel, on_delete=models.CASCADE)
    download = models.FloatField('download')
    upload = models.FloatField('upload')
    lat = models.FloatField('lat')
    lon = models.FloatField('lon')

    def __str__(self):
        return f'{self.best_server.cc}.{self.best_server.name}: [{self.download}]'

    @classmethod
    def get_days_worth_speedtest_datapoints(cls, days=7):
        """
        Gets days worth of speedtest datapoits
        :return: Queryset with data points (list of dicts)
        """
        today = timezone.now() + timedelta(days=1)
        same_day_last_week = today - timedelta(days=days)

        speedtest_object = SpeedtesterModel.objects.filter(created__gte=same_day_last_week,
                                                           created__lt=today).values('created', 'download', 'upload')
        return speedtest_object

    class Meta:
        verbose_name = 'Speed Test'
        verbose_name_plural = 'Speed Tests'
