import os
from distutils.core import setup


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name="django-datarequests",
    version="0.1",
    author="",
    author_email="",
    description="Data Requests Portal for GeoNode projects",
    long_description=(read('README.rst')),
    # Full list of classifiers can be found at:
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 1 - Planning',
    ],
    license="BSD",
    keywords="epidemico geonode data requests",
    url='https://github.com/epidemico/django-datarequests',
    packages=['data_requests', ],
    install_requires=[
      'django-tables2',
      'django-filter'
    ],
    include_package_data=True,
    zip_safe=False,
)
