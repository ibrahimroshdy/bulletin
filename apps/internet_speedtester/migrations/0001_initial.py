# Generated by Django 4.0.7 on 2022-08-29 16:06

import django.utils.timezone
import model_utils.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
                name='ClientModel',
                fields=[
                    (
                        'id',
                        models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                    ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False,
                                                                    verbose_name='created')),
                    ('modified',
                     model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False,
                                                              verbose_name='modified')),
                    ('ip', models.GenericIPAddressField(verbose_name='ipaddress')),
                    ('lat', models.FloatField(verbose_name='lat')),
                    ('lon', models.FloatField(verbose_name='lon')),
                    ('isp', models.CharField(max_length=256, verbose_name='internet service provider')),
                    ('cc', models.CharField(max_length=5, verbose_name='country code')),
                ],
                options={
                    'verbose_name': 'Client',
                    'verbose_name_plural': 'Clients',
                },
        ),
        migrations.CreateModel(
                name='ServersModel',
                fields=[
                    ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False,
                                                                    verbose_name='created')),
                    ('modified',
                     model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False,
                                                              verbose_name='modified')),
                    ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='id')),
                    ('url', models.URLField(verbose_name='url')),
                    ('lat', models.FloatField(verbose_name='lat')),
                    ('lon', models.FloatField(verbose_name='lon')),
                    ('name', models.CharField(max_length=256, verbose_name='city')),
                    ('country', models.CharField(max_length=256, verbose_name='country')),
                    ('cc', models.CharField(max_length=5, verbose_name='country code')),
                    ('sponsor', models.CharField(max_length=256, verbose_name='sponsor')),
                    ('host', models.CharField(max_length=256, verbose_name='host')),
                    ('d', models.FloatField(verbose_name='d')),
                    ('latency', models.FloatField(blank=True, null=True, verbose_name='latency')),
                ],
                options={
                    'verbose_name': 'Server',
                    'verbose_name_plural': 'Servers',
                },
        ),
        migrations.CreateModel(
                name='SpeedtesterModel',
                fields=[
                    (
                        'id',
                        models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                    ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False,
                                                                    verbose_name='created')),
                    ('modified',
                     model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False,
                                                              verbose_name='modified')),
                    ('download', models.FloatField(verbose_name='download')),
                    ('upload', models.FloatField(verbose_name='upload')),
                    ('lat', models.FloatField(verbose_name='lat')),
                    ('lon', models.FloatField(verbose_name='lon')),
                    ('best_server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                      to='internet_speedtester.serversmodel')),
                    ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                 to='internet_speedtester.clientmodel')),
                ],
                options={
                    'verbose_name': 'Speed Test',
                    'verbose_name_plural': 'Speed Tests',
                },
        ),
    ]
