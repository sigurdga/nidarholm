from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template.defaultfilters import slugify
from django.conf import settings
from news.models import Story
from news.forms import StoryForm
from pages.models import FlatPage
from django.views.generic import list_detail
from django.template.context import RequestContext

def story_list(request, page=1):
    if page == 1:
        infopage = get_object_or_404(FlatPage, url__exact='/', sites__id__exact=settings.SITE_ID)
    else:
        infopage = None

    return list_detail.object_list(request,
                                   queryset=Story.objects.for_user(request.user).filter(parent=None),
                                   page=page,
                                   template_name='news/main.html',
                                   extra_context={'infopage': infopage})

def new_story(request, id=None):
    """slug is the slug of the parent, may be null"""
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            #story.slug = slugify(story.title)
            story.save()
            return HttpResponseRedirect('/')
    else:
        story = Story()
        if id:
            parent = get_object_or_404(Story, id=id)
            story.parent = parent
        form = StoryForm(instance=story)
    return render_to_response('forum/new_debate.html', {'form': form}, context_instance=RequestContext(request))
