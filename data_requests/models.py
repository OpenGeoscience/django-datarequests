from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django_tables2 import tables
from django_tables2.utils import A
from geonode.base.models import TopicCategory

__author__ = 'mbertrand'


DATA_STATUS_CHOICES = (
        ('Open', 'Open'),
        ('Closed', 'Closed'),
        ('Duplicate', 'Duplicate'),
        ('Rejected', 'Rejected'),
)


class DataRequest(models.Model):
    """
    Model for a data request.
    """
    name = models.CharField(_('data name'), max_length=255, null=False, blank=False)
    description = models.TextField(_('data description'),  null=False, blank=False)
    requestor_name = models.CharField(_('requestor name'), max_length=255, unique=False)
    requestor_email = models.CharField(_('requestor email'), max_length=255, null=False, blank=False)
    source = models.CharField(_('data source'), max_length=255, null=False, blank=False)
    url = models.TextField(_('data source URL'), blank=True, null=True)
    data_license_url = models.TextField(_('data license URL'), blank=True, null=True)
    metadata_url = models.TextField(_('metadata URL'), blank=True, null=True)
    data_url = models.TextField(_('imported data link'), blank=True, null=True)
    status = models.CharField(choices=DATA_STATUS_CHOICES, default='Open', max_length=10)
    created_dttm = models.DateTimeField(auto_now_add=True)
    modified_dttm = models.DateTimeField(auto_now=True)


class DataRequestTable(tables.Table):
    """
    Django-table2 Table for DataRequest objects
    """
    name = tables.columns.LinkColumn('data_request_detail', args=[A('pk')], verbose_name=_("Name"))
    source = tables.columns.Column(verbose_name=_("Data source"))
    status = tables.columns.Column(verbose_name=_("Status"))
    modified_dttm = tables.columns.Column(verbose_name=_("Modified"))

    fields = ['name', 'source', 'status', 'modified_dttm']

    class Meta:
        model = DataRequest
        exclude = ['description', 'requestor_name', 'requestor_email', 'url', 'data_license_url', 'metadata_url',
                   'data_url', 'created_dttm', 'id']
        attrs = {'class': 'table table-striped table-bordered table-condensed'}

