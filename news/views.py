from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template.defaultfilters import slugify
from django.conf import settings
from news.models import Story
from news.forms import StoryForm
from pages.models import FlatPage
from django.views.generic import list_detail, date_based
from django.template.context import RequestContext

def story_list(request):
    infopage = get_object_or_404(FlatPage, url__exact='/', sites__id__exact=settings.SITE_ID)

    return list_detail.object_list(request,
            queryset=Story.objects.for_user(request.user).filter(parent=None).order_by('-pub_date')[:5],
            template_name='news/main.html',
            extra_context={'infopage': infopage})

def story_archive(request):
    queryset = Story.objects.for_user(request.user).filter(parent=None)
    date_field = "pub_date"
    return date_based.archive_index(request, queryset, date_field)

def story_year(request, year):
    queryset = Story.objects.for_user(request.user).filter(parent=None)
    date_field = "pub_date"
    return date_based.archive_year(request, year, queryset, date_field, make_object_list=True)

def story_detail(request, year, month, day, slug):
    queryset = Story.objects.for_user(request.user).filter(parent=None)
    date_field = "pub_date"
    month_format = "%m"
    return date_based.object_detail(request, year, month, day, queryset, date_field, month_format=month_format, slug=slug, allow_future=True)
    

def edit_story(request, id):
    story = get_object_or_404(Story, id=id)
    if request.user != story.user:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        form = StoryForm(data=request.POST, instance=story)
        if form.is_valid():
            story.save()
            return HttpResponseRedirect('/')
    else:
        form = StoryForm(instance=story)
    return render_to_response('forum/new_debate.html', {'form': form}, context_instance=RequestContext(request))

def new_story(request, id=None):
    """slug is the slug of the parent, may be null"""
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            story.save()
            return HttpResponseRedirect('/')
    else:
        story = Story()
        initial = {}
        if id:
            parent = get_object_or_404(Story, id=id)
            story.parent = parent
            initial['title'] = "Re: " + parent.title
            initial['group'] = parent.group
        form = StoryForm(instance=story, initial=initial)
    return render_to_response('forum/new_debate.html', {'form': form}, context_instance=RequestContext(request))
