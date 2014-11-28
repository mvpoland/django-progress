from contextlib import contextmanager
import datetime
import os
import subprocess
import sys

from logging import getLogger

logger = getLogger(__name__)

try:
    from django.utils.timezone import now
except ImportError:
    now = datetime.datetime.now

try:
    from django.views.debug import ExceptionReporter
except ImportError:
    # prevent pip install to crash
    pass


def get_git_version():
    git_dir = os.path.abspath(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            '..',
            '.git'
        )
    )
    try:
        # Python 2.7 has subprocess.check_output
        # 2.6 needs this longer version
        git_info = subprocess.Popen(['git', '--git-dir=%s' % git_dir, 'log', '--pretty=%ct %h', '-1'], stdout=subprocess.PIPE).communicate()[0].split()
        git_time = datetime.datetime.fromtimestamp(float(git_info[0]))
    except Exception:
        git_time = now()
        git_info = ('', '0000000')
    return git_time.strftime('%Y.%m.%d') + '.' + git_info[1]

__version__ = get_git_version()
VERSION = __version__


class ProgressException(Exception):
    def __init__(self, description):
        self.description = description

    def __unicode__(self):
        return self.description


import threading
tls = threading.local()


def with_progress(collection, name=None, count=-1):
    """
    This is a generator for keeping track of the progress of long running tasks.

    Example:

    >>> for item in with_progress(list_of_items, name='My hardcore processing action'):
    >>>     # heavy processing action with item

    name can be anything, but is limited to 64 characters.

    In the Django Admin, you can see an overview of all running processes with their
    progress and an estimated time of arrival/completion. This information is updated
    at a minimum interval of 5 seconds.
    """
    from djprogress.models import Progress

    if not name:
        raise ProgressException('This with_progress call has no name')

    count = count if count > -1 else len(collection)
    start_ts = now()
    last_updated = start_ts
    items_since_retarget = 0

    ### Keep track of parent progresses using threading.local
    if not hasattr(tls, 'djprogress__stack'):
        tls.djprogress__stack = []
    parent_progress = None
    if tls.djprogress__stack:
        parent_progresses = Progress.objects.filter(pk=tls.djprogress__stack[-1])
        while tls.djprogress__stack and not parent_progresses:
            tls.djprogress__stack.pop()
            parent_progresses = Progress.objects.filter(pk=tls.djprogress__stack[-1])
        if parent_progresses:
            parent_progress = parent_progresses[0]

    progress = Progress.objects.create(name=name, total=count, parent=parent_progress)

    tls.djprogress__stack.append(progress.pk)
    for i, item in enumerate(collection):
        yield item

        ts = now()

        if i % 1000 == 0:
            # After each block of 1000 items, retarget the estimation, to
            # account for mid-term fluctuations.
            start_ts = ts
            items_since_retarget = 0

        if (ts - last_updated).seconds > 5:
            # After 5 seconds since last_updated, update the Progress instance
            seconds_elapsed = (ts - start_ts).seconds
            seconds_to_go = seconds_elapsed * float(count-i) / float(items_since_retarget+1)
            eta = ts + datetime.timedelta(seconds=seconds_to_go)

            progress.eta = eta
            progress.current = i + 1
            progress.save()
            last_updated = ts

        items_since_retarget = items_since_retarget + 1

    progress.delete()
    if tls.djprogress__stack:
        tls.djprogress__stack.pop()


@contextmanager
def progress_error_reporter():
    """
    Use this wrapper around your progress loops like this:

    >>> with progress_error_reporter():
    >>>     for item in with_progress(collection, name='my long process that can throw errors')
    >>>         # heavy processing actions with sometimes an exception :-)

    When an exception gets raised from inside the body of your for-loop, it will be
    caught and the progress bar will show a link to the exception. The exception is rendered
    by the standard exception reporter, containing the full stack trace with variables.
    """
    try:
        yield
    except:
        try:
            if hasattr(tls, 'djprogress__stack'):
                from djprogress.models import Progress

                progress_id = tls.djprogress__stack.pop()

                progress = Progress.objects.get(pk=progress_id)
                exc_type, exc_value, exc_traceback = sys.exc_info()
                er = ExceptionReporter(None, exc_type, exc_value, exc_traceback)
                html = er.get_traceback_html()
                progress.exception = html
                progress.save()
        except Exception as e:
            # When the error reporter fails for whatever reason, catch and log the
            # exception here so that our regular code flow isn't interrupted. The
            # 'raise' statement will take care of the rest.
            logger.exception(e)
        raise
