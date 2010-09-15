from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template.defaultfilters import slugify
from news.models import Story
from news.forms import StoryForm

def story_list(request):
    story_list = Story.objects.filter(parent=None)
    paginator = Paginator(story_list, 25)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        stories = paginator.page(page)
    except (EmptyPage, InvalidPage):
        stories = paginator.page(paginator.num_pages)

    return render_to_response('forum/list.html', {'debate': stories})

def story(request, slug):
    debate = get_object_or_404(Story, slug=slug)
    return render_to_response('forum/tree.html', {'debate': debate})

def new_story(request, slug=None):
    """slug is the slug of the parent, may be null"""
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            story.slug = slugify(story.title)
            story.save()
            return HttpResponseRedirect('/forum')
    else:
        parent = get_object_or_404(Story, slug=slug)
        story = Story()
        story.parent = parent
        form = StoryForm(instance=story)
    return render_to_response('forum/new_debate.html', {'form': form})