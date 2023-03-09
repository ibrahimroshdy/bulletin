# Generated by Django 4.1.6 on 2023-03-09 17:37

import django.utils.timezone
import model_utils.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
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
                name='TwitterAccount',
                fields=[
                    ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False,
                                                                    verbose_name='created')),
                    ('modified',
                     model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False,
                                                              verbose_name='modified')),
                    ('username',
                     models.CharField(max_length=15, primary_key=True, serialize=False, verbose_name='Username')),
                    (
                    'twt_bearer_token', models.CharField(max_length=256, unique=True, verbose_name='TWT Bearer Token')),
                    (
                    'twt_consumer_key', models.CharField(max_length=256, unique=True, verbose_name='TWT Consumer Key')),
                    ('twt_consumer_secret',
                     models.CharField(max_length=256, unique=True, verbose_name='TWT Consumer Key')),
                    ('twt_access_key',
                     models.CharField(max_length=256, unique=True, verbose_name='TWT Consumer Secret')),
                    ('twt_access_secret', models.CharField(max_length=256, unique=True, verbose_name='TWT Access Key')),
                    ('slk_bot_token', models.CharField(max_length=256, unique=True, verbose_name='Slack Bot Token')),
                    (
                    'slk_bot_channel', models.CharField(max_length=256, unique=True, verbose_name='Slack Bot Channel')),
                    ('logo', models.ImageField(upload_to='accounts/', verbose_name='Logo')),
                    ('tweet_image_template',
                     models.ImageField(upload_to='accounts/', verbose_name='Tweet Image Template')),
                ],
                options={
                    'verbose_name': 'Twitter Account',
                    'verbose_name_plural': 'Twitter Accounts',
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
                    ('id', models.CharField(max_length=90, primary_key=True, serialize=False, verbose_name='ID')),
                    ('country', models.CharField(max_length=256, verbose_name='Country')),
                    ('cc', models.CharField(max_length=5, verbose_name='Country Code')),
                    ('active', models.BooleanField(default=True, verbose_name='Active')),
                ],
                options={
                    'verbose_name': 'Where On Earth ID',
                    'verbose_name_plural': 'Where On Earth IDs',
                },
        ),
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
                    ('tweet_text', models.TextField(max_length=280, verbose_name='Tweet Text')),
                    ('is_tweeted', models.BooleanField(default=False, verbose_name='Is Tweeted')),
                    ('tweet_date', models.DateTimeField(default=None, null=True, verbose_name='Tweeted Date')),
                    ('has_image', models.BooleanField(default=False, verbose_name='Has Image')),
                    ('tweet_image', models.ImageField(upload_to='tweets', verbose_name='Tweet Image')),
                    ('twitter_account',
                     models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social.twitteraccount')),
                ],
                options={
                    'verbose_name': 'Tweet',
                    'verbose_name_plural': 'Tweets',
                },
                managers=[
                    ('random_tweet', django.db.models.manager.Manager()),
                ],
        ),
    ]
