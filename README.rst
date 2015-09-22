django-datarequests
========================

Data Request Portal app for Django/GeoNode projects.

Installation
------------

Add this line to your requirements.txt file:

```
-e git+https://github.com/epidemico/django-datarequests.git#egg
```

pip install -r requirements.txt

Add 'data_requests' and 'django_tables2' to your INSTALLED_APPS setting

Add the data_requests urls to your project's urls.py file:
```
import data_requests

urlpatterns = patterns('',
    ...
    url(r'^datarequests/', include('data_requests.urls')),
 ) + urlpatterns

```

python manage.py syncdb

Running tests
------------
python manage.py test data_requests

