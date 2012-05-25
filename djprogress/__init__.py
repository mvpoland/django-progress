import datetime
import os
import subprocess

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
        git_time = datetime.datetime.now()
        git_info = ('', '0000000')
    return git_time.strftime('%Y.%m.%d') + '.' + git_info[1]

__version__ = get_git_version()
VERSION = __version__


class ProgressException(Exception):
    def __init__(self, description):
        self.description = description
    
    def __unicode__(self):
        return self.description


def with_progress(collection, name=None):
    '''
    This is a generator for keeping track of the progress of long running tasks.
    
    Example:
    
    >>> for item in with_progress(list_of_items, name='My hardcore processing action'):
    >>>     # heavy processing action with item
    
    name can be anything, but is limited to 64 characters.
    
    In the Django Admin, you can see an overview of all running processes with their
    progress and an estimated time of arrival/completion. This information is updated
    at a minimum interval of 5 seconds.
    '''
    
    from djprogress.models import Progress
    
    if not name:
        raise ProgressException('This with_progress call has no name')
    
    count = len(collection)
    start_ts = datetime.datetime.now()
    last_updated = start_ts
    
    progress = Progress.objects.create(name=name, total=count)
    
    for i, item in enumerate(collection):
        yield item
        ts = datetime.datetime.now()
        if (ts - last_updated).seconds > 5:
            seconds_elapsed = (ts - start_ts).seconds
            seconds_to_go = seconds_elapsed * float(count) / float(i+1)
            eta = ts + datetime.timedelta(seconds=seconds_to_go)
            
            progress.eta = eta
            progress.current = i + 1
            progress.save()
            last_updated = ts
    
    progress.delete()

