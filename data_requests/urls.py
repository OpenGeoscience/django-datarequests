from django.conf.urls import url
from django.conf import settings
from . import views

DATA_REQUESTS_PER_PAGE = getattr(settings, 'DATA_REQUESTS_PER_PAGE', 10)

urlpatterns = [
    url(r'^$', views.DataRequestList.as_view(
        template_name="data_requests/request_list.html",
        table_pagination={"per_page": DATA_REQUESTS_PER_PAGE}),
        name='data_request_list'),
    url(r'^edit/(?P<request_id>[^/]*)$', views.request_edit,
        name='data_request_edit'),
    url(r'^detail/(?P<pk>[^/]*)/$', views.DataRequestDetailView.as_view(
        template_name='data_requests/request_detail.html'),
        name='data_request_detail'),
    url(r'^new$', views.request_new, name='data_request_new'),

]
