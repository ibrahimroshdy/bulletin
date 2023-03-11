from django.db import models
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from model_utils.models import TimeStampedModel

from .helpers import SingletonModel, TweetManager, TweetSystemStatus


class TwitterAccount(TimeStampedModel):
    """Model class representing a twitter account in bulletin"""
    username = models.CharField('Username', primary_key=True, max_length=15)
    twt_bearer_token = models.CharField('TWT Bearer Token', max_length=256, unique=True)
    twt_consumer_key = models.CharField('TWT Consumer Key', max_length=256, unique=True)
    twt_consumer_secret = models.CharField('TWT Consumer Key', max_length=256, unique=True)
    twt_access_key = models.CharField('TWT Consumer Secret', max_length=256, unique=True)
    twt_access_secret = models.CharField('TWT Access Key', max_length=256, unique=True)
    slk_bot_token = models.CharField('Slack Bot Token', max_length=256, unique=True)
    slk_bot_channel = models.CharField('Slack Bot Channel', max_length=256, unique=True, )
    logo = models.ImageField('Logo', upload_to=f'accounts/')
    tweet_image_template = models.ImageField('Tweet Image Template', upload_to='accounts/', )

    def __str__(self):
        return f'{self.username}'

    def logo_tag(self):
        """
        Returns an HTML tag for the image associated with this model instance.
        :return: str: An HTML `img` tag with the URL of the image as the `src` attribute.
        """
        if self.logo:
            return format_html(f'<img src="{self.logo.url}" width="50" height="50"/>')
        return mark_safe('<strong>There is no logo for this account.<strong>')

    def tweet_image_template_tag(self):
        """
        Returns an HTML tag for the image associated with this model instance.
        :return: str: An HTML `img` tag with the URL of the image as the `src` attribute.
        """
        if self.tweet_image_template:
            return format_html(f'<img src="{self.tweet_image_template.url}" width="200" height="112"/>')
        return mark_safe('<strong>There is no image template for this account.<strong>')

    logo.short_description = 'Logo'
    logo.allow_tags = True

    tweet_image_template.short_description = 'Twt Image Template'
    tweet_image_template.allow_tags = True

    class Meta:
        verbose_name = 'Twitter Account'
        verbose_name_plural = 'Twitter Accounts'


class TweetModel(TimeStampedModel):
    """A model representing a tweet.

    Attributes:
        tweet_text (TextField): The text of the tweet, with a max length of 280 characters.
        is_tweeted (BooleanField): Whether the tweet has been tweeted or not (default: False).
        tweet_date (DateTimeField): The date and time the tweet was tweeted (default: None).
        has_image (BooleanField): Whether the tweet has an image or not (default: False).
        tweet_image (ImageField): The image associated with the tweet.

    Methods:
        clean (): Performs model-level validation and data cleaning before saving the instance.
        image_tag (): Returns an HTML `img` tag for the tweet's image.

    """
    twitter_account = models.ForeignKey(TwitterAccount, on_delete=models.CASCADE)
    tweet_text = models.TextField('Tweet Text', max_length=280)
    is_tweeted = models.BooleanField('Is Tweeted', default=False)
    tweet_date = models.DateTimeField('Tweeted Date', default=None, null=True)
    has_image = models.BooleanField('Has Image', default=False)
    tweet_image = models.ImageField('Tweet Image', upload_to='tweets')

    # Random Tweet field by tweet manager
    random_tweet = TweetManager()

    # Defulats objects manager
    objects = models.Manager()

    def __str__(self):
        return f'{self.tweet_date}.{self.is_tweeted}'

    def clean(self):
        """
        Perform model-level validation and clean up any data before saving the model instance.

        Raises:
            ValidationError: If the validation fails, a ValidationError exception is raised with a message describing the error.

        Example:
            >> model_instance.clean()
            ValidationError: The 'name' field must not be longer than 50 characters.
        """
        if self.tweet_image:
            self.has_image = True
        if self.tweet_date:
            self.is_tweeted = True

    def image_tag(self):
        """
        Returns an HTML tag for the image associated with this model instance.
        :return: str: An HTML `img` tag with the URL of the image as the `src` attribute.
        """
        if self.tweet_image:
            return format_html(f'<img src="{self.tweet_image.url}" width="800" height="450"/>')
        return mark_safe('<strong>There is no image for this entry.<strong>')

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    class Meta:
        verbose_name = 'Tweet'
        verbose_name_plural = 'Tweets'


class TweetSystemModel(SingletonModel):
    """A singleton model to store the current status of the tweeting system.

    Attributes:
        status (str): The current status of the tweeting system.
        created (datetime): The datetime when the status was created.
        modified (datetime): The datetime when the status was last updated.
        message (str): Additional message with the status.

    Methods:
        set_error (message='NO MESSAGE ATTACHED'): Sets the status to 'error' and updates the message.
        set_maintenance (message='NO MESSAGE ATTACHED'): Sets the status to 'maintenance' and updates the message.
        set_working (message='NO MESSAGE ATTACHED'): Sets the status to 'working' and updates the message.

    """

    def __str__(self):
        return f'{self.status}'

    def set_error(self, message='NO MESSAGE ATTACHED'):
        """
        Sets the status of the tweeting system to 'error' and updates the message.

        Args:
            message (str): A message describing the error.

        Example:
            >> tweet_status = TweetSystemModel.load()
            >> tweet_status.set_error("The tweeting system is down.")
            >> tweet_status.status
            'error'
        """
        self.status = TweetSystemStatus.ERROR.name
        self.message = message
        self.save()

    def set_maintenance(self, message='NO MESSAGE ATTACHED'):
        """
        Sets the status of the tweeting system to 'maintenance' and updates the message.

        Args:
            message (str): A message describing the maintenance.

        Example:
            >> tweet_status = TweetSystemModel.load()
            >> tweet_status.set_maintenance("The tweeting system is undergoing maintenance.")
            >> tweet_status.status
            'maintenance'
        """
        self.status = TweetSystemStatus.MAINTENANCE.name
        self.message = message
        self.save()

    def set_working(self, message='NO MESSAGE ATTACHED'):
        """
        Sets the status of the tweeting system to 'working' and updates the message.

        Args:
            message (str): A message describing the status of the system.

        Example:
            >> tweet_status = TweetSystemModel.load()
            >> tweet_status.set_working("The tweeting system is working.")
            >> tweet_status.status
            'working'
        """
        self.status = TweetSystemStatus.WORKING.name
        self.message = message
        self.save()

    class Meta:
        verbose_name = 'Tweet System Status'
        verbose_name_plural = 'Tweet System Status'
