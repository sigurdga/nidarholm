from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template.defaultfilters import slugify
from forum.models import Debate
from forum.forms import DebateForm
from django.template.context import RequestContext
from django.views.generic import list_detail

def debate_list(request):

    return list_detail.object_list(request,
                                   queryset=Debate.objects.for_user(request.user).filter(parent=None),
                                   paginate_by=20,
                                   template_name='forum/list.html',
                                   )

def debate_object_detail(request, slug):
    return list_detail.object_detail(request,
                                     Debate.objects.for_user(request.user),
                                     slug=slug,
                                     template_name='forum/debate_detail.html',
                                     )

def new_debate(request, slug=None):
    """slug is the slug of the parent, may be null"""
    if request.method == 'POST':
        form = DebateForm(request.POST)
        if form.is_valid():
            debate = form.save(commit=False)
            debate.user = request.user
            debate.save()
            return HttpResponseRedirect(debate.get_top_url())
    else:
        debate = Debate()
        initial = {}
        if slug:
            parent = get_object_or_404(Debate, slug=slug)
            debate.parent = parent
            initial['title'] = "Re: " + parent.title
            initial['group'] = parent.group
        form = DebateForm(instance=debate, initial=initial)
    return render_to_response('forum/new_debate.html', {'form': form}, context_instance=RequestContext(request))
