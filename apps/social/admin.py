from django.contrib import admin
from import_export.admin import ExportActionMixin, ImportExportModelAdmin

from . import models


@admin.register(models.WoeidModel)
class WoeidAdmin(ImportExportModelAdmin, ExportActionMixin):
    """
    Django admin class for WoeidModel model,
    which is registered with the django admin site.
    This class inherits from ImportExportModelAdmin and ExportActionMixin.
    """
    list_display = ['country', 'active', 'cc', 'id', 'created']
    list_filter = ['country', 'cc', 'active']
    search_fields = ['country', 'cc']
    date_hierarchy = 'created'


@admin.register(models.TweetModel)
class TweetAdmin(ImportExportModelAdmin, ExportActionMixin):
    """
    Django admin class for TweetModel model,
    which is registered with the django admin site.
    This class inherits from ImportExportModelAdmin and ExportActionMixin
    """
    list_display = ['id', 'tweet_text', 'is_tweeted', 'tweet_date', 'has_image']
    list_filter = ['is_tweeted', 'has_image']
    search_fields = ['tweet_text']
    date_hierarchy = 'tweet_date'
    readonly_fields = ['tweet_date', 'has_image', 'is_tweeted', 'tweet_image', 'image_tag']


@admin.register(models.TweetSystemModel)
class TweetSystemAdmin(ImportExportModelAdmin, ExportActionMixin):
    """
    Django admin class for TweetSystemModel model,
    which is registered with the django admin site.
    This class inherits from ImportExportModelAdmin and ExportActionMixin.
    """
    list_display = ['status', 'message']
    date_hierarchy = 'modified'
    readonly_fields = ['status', 'message']
