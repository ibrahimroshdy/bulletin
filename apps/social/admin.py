from django.contrib import admin
from import_export.admin import ExportActionMixin, ImportExportModelAdmin

from . import models


@admin.register(models.WoeidModel)
class WoeidAdmin(ImportExportModelAdmin, ExportActionMixin):
    list_display = ['country', 'active', 'cc', 'id', 'created']
    list_filter = ['country', 'cc', 'active']
    search_fields = ['country', 'cc']
    date_hierarchy = 'created'
