from django.contrib import admin
from import_export.admin import ExportActionMixin, ImportExportModelAdmin

from . import models


@admin.register(models.WoeidModel)
class WoeidAdmin(ImportExportModelAdmin, ExportActionMixin):
    list_display = ['country', 'active', 'cc', 'id', 'created']
    list_filter = ['country', 'cc', 'active']
    search_fields = ['country', 'cc']
    date_hierarchy = 'created'


@admin.register(models.TweetModel)
class TweetAdmin(ImportExportModelAdmin, ExportActionMixin):
    list_display = ['id', 'tweet_text', 'is_tweeted', 'tweet_date']
    list_filter = ['is_tweeted']
    search_fields = ['tweet_text']
    date_hierarchy = 'tweet_date'
    readonly_fields = ['tweet_date']
