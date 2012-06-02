from django.template.context import RequestContext
from django.shortcuts import render_to_response

from djprogress.models import Progress
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def overview(request):
    progresses = Progress.objects.order_by('pk')
    context = {'progresses': progresses}
    return render_to_response('djprogress/overview.html', context, context_instance=RequestContext(request))
