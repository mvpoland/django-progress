from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


class Progress(models.Model):
    name = models.CharField(max_length=64, db_index=True)
    current = models.IntegerField(default=0)
    total = models.IntegerField(default=100)
    eta = models.DateTimeField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, db_index=True)
    parent = models.ForeignKey(
        'Progress',
        blank=True,
        null=True,
        related_name='children',
        on_delete=models.CASCADE
    )
    exception = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'progress'
        verbose_name_plural = 'progresses'

    def __str__(self):
        return '{}: {}/{}'.format(self.name, self.current, self.total)
    
    def is_just_now_updated(self):
        return (timezone.now() - self.last_updated).seconds < 7

