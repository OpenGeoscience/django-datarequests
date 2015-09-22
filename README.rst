django-datarequests
========================

Installation
------------

Add this line to your requirements.txt file:

```
-e git+https://github.com/epidemico/django-datarequests.git#egg=django-datarequests-0.1
```

pip install -r requirements.txt

Add 'data_requests' and 'django_tables2' to your INSTALLED_APPS setting

python manage.py syncdb

Running tests
------------
python manage.py test data_requests

