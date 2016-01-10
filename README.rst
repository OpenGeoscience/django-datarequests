django-datarequests
========================

Data Request Portal app for Django/GeoNode projects.

Installation
------------

- Add this line to your requirements.txt file::

    -e git+https://github.com/OpenGeoscience/django-datarequests.git#egg=django-datarequests

- pip install -r requirements.txt

- Add the following to your INSTALLED_APPS setting::

    INSTALLED_APPS = (
                    ...
                    'data_requests',
                    'django_tables2',

- Add the following to settings.py to enable email notifications::

    DATA_REQUEST_NOTIFY = True
    DATA_REQUEST_EMAILS = [<email_address>,]
    DEFAULT_EMAIL_FROM = <default_from_email>
    EMAIL_USE_TLS = False
    EMAIL_HOST = <your_email_host>
    EMAIL_HOST_USER = <email_host_user>
    EMAIL_HOST_PASSWORD = <email_host_password>
    EMAIL_PORT = <email_host_port>

- Add the data_requests urls to your project's urls.py file::

    import data_requests
    urlpatterns = patterns('',
      ...
      url(r'^datarequests/', include('data_requests.urls')),
    ) + urlpatterns

- Optionally add a link to the datarequests url in site_base.html template::

    {% block extra_tab %}
    <li>
      <a href="/datarequests">Requests</a>
    </li>
    {% endblock %}

- python manage.py syncdb

Running tests
------------
- python manage.py test data_requests

