# Generated by Django 4.0.7 on 2023-02-06 19:53

import django.utils.timezone
import model_utils.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
                name='TweetModel',
                fields=[
                    (
                    'id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                    ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False,
                                                                    verbose_name='created')),
                    ('modified',
                     model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False,
                                                              verbose_name='modified')),
                    ('tweet_text', models.TextField(max_length=280, verbose_name='tweet_text')),
                    ('is_tweeted', models.BooleanField(default=False, verbose_name='tweeted')),
                    ('tweet_date', models.DateTimeField(default=None, null=True, verbose_name='tweeted_date')),
                    ('has_image', models.BooleanField(default=False, verbose_name='has_image')),
                    ('tweet_image', models.ImageField(upload_to='tweets')),
                ],
                options={
                    'verbose_name': 'Tweet',
                    'verbose_name_plural': 'Tweets',
                },
                managers=[
                    ('random_tweet', django.db.models.manager.Manager()),
                ],
        ),
        migrations.CreateModel(
                name='TweetSystemModel',
                fields=[
                    (
                    'id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                    ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False,
                                                                    verbose_name='created')),
                    ('modified',
                     model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False,
                                                              verbose_name='modified')),
                    ('status', models.CharField(
                        choices=[('WORKING', 'working'), ('ERROR', 'error'), ('MAINTENANCE', 'maintenance'),
                                 ('UNKNOWN', 'unknown')], default='UNKNOWN', max_length=20)),
                    ('message', models.TextField(max_length=1000, null=True)),
                ],
                options={
                    'verbose_name': 'Tweet System Status',
                    'verbose_name_plural': 'Tweet System Status',
                },
        ),
        migrations.CreateModel(
                name='WoeidModel',
                fields=[
                    ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False,
                                                                    verbose_name='created')),
                    ('modified',
                     model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False,
                                                              verbose_name='modified')),
                    ('id', models.CharField(max_length=90, primary_key=True, serialize=False, verbose_name='id')),
                    ('country', models.CharField(max_length=256, verbose_name='country')),
                    ('cc', models.CharField(max_length=5, verbose_name='country code')),
                    ('active', models.BooleanField(default=True, verbose_name='active')),
                ],
                options={
                    'verbose_name': 'Where On Earth ID',
                    'verbose_name_plural': 'Where On Earth IDs',
                },
        ),
    ]
