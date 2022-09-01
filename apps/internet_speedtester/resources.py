from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget

from . import models


class SpeedtesterResource(resources.ModelResource):  # pragma: no cover
    id = fields.Field(attribute='id')
    best_server = fields.Field(attribute='best_server', widget=ForeignKeyWidget(models.ServersModel, 'url'))
    client = fields.Field(attribute='client', widget=ForeignKeyWidget(models.ClientModel, 'ip'))

    class Meta:
        model = models.SpeedtesterModel
