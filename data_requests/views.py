from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.views.generic import DetailView
from django_tables2 import SingleTableView
import django_filters
from .models import DataRequest, DataRequestTable
from .forms import DataRequestForm, DataRequestAdminForm


def request_new(request, template='data_requests/request_new.html'):
    """
    View and submit/save a data request form.
    """
    if request.method == "POST":
        # save new request
        form = DataRequestForm(request.POST)
        form.save()
        return HttpResponseRedirect(reverse('data_request_list'))
    else:
        form = DataRequestForm()
        return render_to_response(template, RequestContext(request, {
            "request_form": form
        }))


@login_required
def request_edit(request, request_id,
                 template='data_requests/request_edit.html'):
    """
    Edit a data request.  Available only to Django admins (super-users).
    """
    if not request.user.is_superuser:
        return TemplateResponse(request, '401.html', {}, status=401).render()
    data_request = DataRequest.objects.get(id=request_id)
    if request.method == "POST":
        # save new request
        form = DataRequestAdminForm(request.POST, instance=data_request)
        form.save()
        return HttpResponseRedirect(reverse('data_request_list'))
    else:
        form = DataRequestAdminForm(instance=data_request)
        return render_to_response(template, RequestContext(request, {
            "request_form": form,
            "data_request": data_request
        }))


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
