from django.contrib import admin
from import_export.admin import ExportActionMixin, ImportExportModelAdmin

from . import models, resources


@admin.register(models.SpeedtesterModel)
class SpeedtesterAdmin(ImportExportModelAdmin, ExportActionMixin):  # pragma: no cover
    list_display = ['best_server', 'client', 'download', 'upload', 'created']
    list_filter = ['best_server__country', 'best_server__name', 'best_server__cc']
    search_fields = ['best_server__country', 'best_server__name', 'best_server__cc', 'best_server__url', 'client__isp']
    readonly_fields = ['best_server', 'client']
    date_hierarchy = 'created'
    resource_class = resources.SpeedtesterResource


@admin.register(models.ServersModel)
class ServerAdmin(ImportExportModelAdmin, ExportActionMixin):  # pragma: no cover
    list_display = ['url', 'created', 'name', 'country', 'cc', 'sponsor', 'host']
    list_filter = ['name', 'country', 'cc']
    search_fields = ['name', 'country', 'cc', 'url']
    date_hierarchy = 'created'


@admin.register(models.ClientModel)
class ClientAdmin(ImportExportModelAdmin, ExportActionMixin):  # pragma: no cover)
    list_display = ['cc', 'isp', 'ip']
    list_filter = ['cc', 'isp']
    search_fields = ['cc', 'isp']
    date_hierarchy = 'created'
