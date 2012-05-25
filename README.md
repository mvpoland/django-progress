django-progress
===============

A small Django App for monitoring the progress of various operations using a small and handy API.

Example:
```python
    from djprogress import with_progress
    
    for item in with_progress(list_of_items, name='My hardcore processing action'):
        # heavy processing action with item
```


