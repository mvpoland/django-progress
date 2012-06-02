django-progress
===============

A small Django App for monitoring the progress of various operations using a small and handy API.

Example:
```python
from djprogress import with_progress

for item in with_progress(list_of_items, name='My hardcore processing action'):
    # heavy processing action with item
```

There is a view included where you can get an overview of all running processes and their estimated time of completion.
It makes use of admin media so this pages works out of the box. Here is an example:

![django-progress overview page](https://github.com/citylive/django-progress/raw/master/django_progress.png)

