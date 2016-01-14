from django.contrib import admin

from geonode.base.admin import MediaTranslationAdmin, ResourceBaseAdminForm
from data_requests.models import DataRequest


class DataRequestAdmin(admin.ModelAdmin):
    model = DataRequest
    list_display_links = ('name',)
    list_display = ('id', 'name', 'description', 'url', 'data_url')
    search_fields = ('name', 'url', 'data_url')

admin.site.register(DataRequest, DataRequestAdmin)