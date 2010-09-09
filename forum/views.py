from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template.defaultfilters import slugify
from forum.models import Debate
from forum.forms import DebateForm

def debate_list(request):
    debate_list = Debate.objects.all()
    paginator = Paginator(debate_list, 25)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        debates = paginator.page(page)
    except (EmptyPage, InvalidPage):
        debates = paginator.page(paginator.num_pages)

    return render_to_response('forum/list.html', {'debates': debates})

def debate_tree(request, slug):
    debate = get_object_or_404(Debate, slug=slug)
    return render_to_response('forum/tree.html', {'debate': debate})

def new_debate(request, slug=None):
    """slug is the slug of the parent, may be null"""
    if request.method == 'POST':
        form = DebateForm(request.POST)
        if form.is_valid():
            debate = form.save(commit=False)
            debate.user = request.user
            debate.slug = slugify(debate.title)
            debate.save()
            return HttpResponseRedirect('/forum')
    else:
        parent = get_object_or_404(Debate, slug=slug)
        debate = Debate()
        debate.parent = parent
        form = DebateForm(instance=debate)
    return render_to_response('forum/new_debate.html', {'form': form})
