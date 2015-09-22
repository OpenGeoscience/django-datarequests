from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import DataRequest


class DataRequestForm(forms.ModelForm):
    """
    Form for creating new data requests.
    """
    def __init__(self, *args, **kwargs):
        super(DataRequestForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    url = forms.URLField(label=_('Data source URL'), required=False)
    data_license_url = forms.URLField(label=_('Data license URL'),
                                      required=False)
    metadata_url = forms.URLField(label=_('Metadata URL'), required=False)

    class Meta:
        model = DataRequest
        fields = ['requestor_name', 'requestor_email', 'name', 'description',
                  'source', 'url', 'data_license_url', 'metadata_url']
        exclude = ['status', 'created_dttm', 'modified_dttm', 'data_url']


class DataRequestAdminForm(DataRequestForm):
    """
    Form to edit existing data requests, intended for admins only.
    """
    data_url = forms.URLField(label=_('Link to data'), required=False)

    class Meta:
        model = DataRequest
        fields = ['requestor_name', 'requestor_email', 'name', 'description',
                  'source', 'url', 'data_license_url', 'metadata_url',
                  'data_url', 'status']
        exclude = ['created_dttm', 'modified_dttm']
