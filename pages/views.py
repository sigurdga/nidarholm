from pages.models import FlatPage
from pages.forms import PageForm
from django.template import loader, RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.core.xheaders import populate_xheaders
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_protect
from django.views.generic.list_detail import object_list

DEFAULT_TEMPLATE = 'pages/default.html'

# This view is called from FlatpageFallbackMiddleware.process_response
# when a 404 is raised, which often means CsrfViewMiddleware.process_view
# has not been called even if CsrfViewMiddleware is installed. So we need
# to use @csrf_protect, in case the template needs {% csrf_token %}.
# However, we can't just wrap this view; if no matching flatpage exists,
# or a redirect is required for authentication, the 404 needs to be returned
# without any CSRF checks. Therefore, we only
# CSRF protect the internal implementation.
def flatpage(request, url):
    """
    Public interface to the flat page view.

    Models: `flatpages.flatpages`
    Templates: Uses the template defined by the ``template_name`` field,
        or `flatpages/default.html` if template_name is not defined.
    Context:
        flatpage
            `flatpages.flatpages` object
    """
    if not url.endswith('/') and settings.APPEND_SLASH:
        return HttpResponseRedirect("%s/" % request.path)
    if not url.startswith('/'):
        url = "/" + url
    f = get_object_or_404(FlatPage, url__exact=url, sites__id__exact=settings.SITE_ID)
    return render_flatpage(request, f)

@csrf_protect
def render_flatpage(request, f):
    """
    Internal interface to the flat page view.
    """
    # If registration is required for accessing this page, and the user isn't
    # logged in, redirect to the login page.
    #if f.registration_required and not request.user.is_authenticated():
    #    from django.contrib.auth.views import redirect_to_login
    #    return redirect_to_login(request.path)
    #if f.template_name:
    #    t = loader.select_template((f.template_name, DEFAULT_TEMPLATE))
    #else:
    t = loader.get_template(DEFAULT_TEMPLATE)

    # To avoid having to always use the "|safe" filter in flatpage templates,
    # mark the title and content as already safe (since they are raw HTML
    # content in the first place).
    f.title = mark_safe(f.title)
    f.content_html = mark_safe(f.content_html)

    c = RequestContext(request, {
        'flatpage': f,
    })
    response = HttpResponse(t.render(c))
    populate_xheaders(request, response, FlatPage, f.id)
    return response

def edit_flatpage(request, id):
    if request.method == 'POST':
        flatpage = get_object_or_404(FlatPage, id=id)
        form = PageForm(request.POST, instance=flatpage)
        if form.is_valid():
            form.save(commit=False)
            flatpage.save()
            return HttpResponseRedirect(flatpage.url)
    else:
        flatpage = get_object_or_404(FlatPage, id=id)
        form = PageForm(instance=flatpage)
    return render_to_response('pages/edit_page.html', {'form': form}, context_instance=RequestContext(request))

def new_flatpage(request):
    if request.method == 'POST':
        flatpage = FlatPage()
        form = PageForm(requst.POST, instance=flatpage)
        if form.is_valid():
            form.save(commit=False)
            flatpage.user = request.user
            flatpage.save()
            return HttpResponseRedirect(flatpage.url)
    else:
        flatpage = FlatPage()
        form = PageForm(instance=flatpage)
    return render_to_response('pages/new_page.html', {'form': form}, context_instance=RequestContext(request))

def flatpage_list(request):
    queryset = FlatPage.objects.for_user(request.user)
    return object_list(request, queryset)
