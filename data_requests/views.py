import django_filters
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.template.loader import render_to_string
from django.views.generic import DetailView
from django_tables2 import SingleTableView
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from urlparse import urljoin
from data_requests.models import DataRequest, DataRequestTable
from data_requests.forms import DataRequestForm, DataRequestAdminForm


DEFAULT_LIST_PARAMS = "?status=Open&sort=-modified_dttm"


def request_new(request, template='data_requests/request_new.html'):
    """
    View and submit/save a data request form.
    """
    if request.method == "POST":
        # save new request
        form = DataRequestForm(request.POST)
        if form.is_valid():
            data_request = form.save()
            if settings.DATA_REQUEST_NOTIFY:
                notify(data_request, request.user)
            return HttpResponseRedirect(reverse('data_request_list') +
                                        DEFAULT_LIST_PARAMS)
    else:
        if request.user.is_anonymous():
            form = DataRequestForm()
        else:
            form = DataRequestForm(initial={
                'requestor_name': request.user.get_full_name(),
                'requestor_email': request.user.email})
    return render_to_response(template, RequestContext(request, {
        "request_form": form
    }))


@login_required
def request_edit(request, request_id,
                 template='data_requests/request_edit.html'):
    """
    Edit a data request.  Available only to Django admins (super-users).
    """
    data_request = DataRequest.objects.get(id=request_id)
    if (not request.user.is_superuser and
                request.user.email != data_request.requestor_email):
        return TemplateResponse(request, '401.html', {}, status=401).render()

    if request.method == "POST":
        # save new request
        form = DataRequestAdminForm(request.POST, instance=data_request)
        if form.is_valid():
            form.save()
            if settings.DATA_REQUEST_NOTIFY:
                notify(data_request, request.user)
            return HttpResponseRedirect(reverse('data_request_list') +
                                        DEFAULT_LIST_PARAMS)
    else:
        form = DataRequestAdminForm(instance=data_request)
    return render_to_response(template, RequestContext(request, {
        "request_form": form,
        "data_request": data_request
    }))


def notify(data_request, user):
    """
    Send email notifications about a new/updated datarequest
    """
    req_url = urljoin(settings.SITEURL,
              reverse('data_request_detail', args=(data_request.id,)))
    msg_plain = render_to_string('data_requests/email.txt',
                                 {
                                     'data_request': data_request,
                                     'data_request_url': req_url
                                 })
    if user.is_anonymous() or user.email == data_request.requestor_email:
        sender = data_request.requestor_email
        recipients = settings.DATA_REQUEST_EMAILS
    else:
        sender = settings.DEFAULT_FROM_EMAIL
        recipients = (data_request.requestor_email,)
    send_mail(_('Data request update - {}'.format(data_request.name)),
              msg_plain, sender,
              recipients, fail_silently=True)


class DataRequestDetailView(DetailView):
    """
    Display details about a data request
    """
    model = DataRequest

    def get_context_data(self, **kwargs):
        context = super(DataRequestDetailView, self).get_context_data(**kwargs)
        return context


class PagedFilteredTableView(SingleTableView):
    """
    SingleTableView with filtering and paging capabilities
    """
    filter_class = None
    context_filter_name = 'filter'

    def get_queryset(self, **kwargs):
        qs = super(PagedFilteredTableView, self).get_queryset()
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super(PagedFilteredTableView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        return context


class DataRequestFilter(django_filters.FilterSet):
    """
    Filters for data requests: status and source fields
    """
    source = django_filters.ChoiceFilter()

    def __init__(self, *args, **kwargs):
        super(DataRequestFilter, self).__init__(*args, **kwargs)
        choose_all = ('', 'All')
        sources = list(DataRequest.objects.all().values_list(
            "source", "source").distinct())
        sources.sort()
        sources.insert(0, choose_all)
        statuses = list(self.filters['status'].extra['choices'])
        statuses.insert(0, choose_all)

        self.filters['source'].extra.update(
            {
                'choices': sources
            })
        self.filters['status'].extra.update(
            {
                'choices': statuses

            })
    class Meta:
        model = DataRequest
        fields = ['status', 'source']


class DataRequestList(PagedFilteredTableView):
    """
    Creates a tabular, filtered, paged list of data requests
    """
    model = DataRequest
    table_class = DataRequestTable
    filter_class = DataRequestFilter
