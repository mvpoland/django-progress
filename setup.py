from setuptools import setup, find_packages

import djprogress

setup(
    name = "django-progress",
    version = djprogress.__version__,
    url = 'http://github.com/citylive/django-progress',
    license = 'BSD',
    description = "Django Progress",
    long_description = open('README.md','r').read(),
    author = 'Jef Geskens',
    packages = find_packages(),
    package_data = {'djprogress': [
                    'templates/*.html', 'templates/*/*.html', 'templates/*/*/*.html'
                ],},
    zip_safe=False, # Don't create egg files, Django cannot find templates in egg files.
    include_package_data=True,
    classifiers = [
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Framework :: Django',
    ],
)

