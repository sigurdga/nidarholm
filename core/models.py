from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group

from markdown import markdown

import re
from vault.models import UploadedFile
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.db.models.query_utils import Q
from django.conf import settings

def replace_references(match_obj):
    # can the parsing be stricter, please?
    description = match_obj.group('description')
    path = match_obj.group('path')
    try:
        img_id, size = path.split('/')
        img_id = int(img_id)
    except ValueError:
        img_id = int(path)
        size = settings.DEFAULT_IMAGE_SIZE
    try:
        file_to_preview = UploadedFile.objects.get(id=img_id)
    except UploadedFile.DoesNotExist:
        return ""
    if file_to_preview.is_image():
        return """<div class="preview">
        <img src="{path}" alt="{description}"/>
        <p class="caption">{description}</p></div>""".format(
            path=reverse('vault.views.send_file', kwargs={'id':img_id, 'size': size}),
            description=description)
    else:
        return """<div class="preview">
        <h2>{filename}</h2>
        <p>Type: {content_type}</p>
        <p class="caption">{description}</p>
        <p><a href="{path}">Last ned</a></p>
        <p><a href="{info_path}">Informasjon</a></p>
        </div>""".format(
            path=reverse('vault.views.send_file', kwargs={'id':img_id}),
            info_path=file_to_preview.get_absolute_url(),
            description=description,
            filename=file_to_preview.filename,
            content_type=file_to_preview.content_type)



def extend_markdown(markdown_content):
    parsed = []
    pattern = re.compile(r'\!\[(?P<description>.*?)\]\[(?P<path>\d+(?:\/\d+)?)\]')
    for line in markdown_content.split('\n'):
        if line.find('![') > -1:
            a = pattern.sub(replace_references, line)
            parsed.append(a)
        else:
            parsed.append(line)

    return markdown('\n'.join(parsed))

class CommonManager(models.Manager):

    def for_user(self, user=None):
        if user and user.is_authenticated():
            return self.get_query_set().filter(Q(group=None) | Q(group__user=user))
        else:
            return self.get_query_set().filter(group=None)

class TextEntry(models.Model):
    title = models.CharField(_('title'), max_length=60)
    slug = models.CharField(_('slug'), max_length=60)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)
    user = models.ForeignKey(User, verbose_name=_('created by'))
    group = models.ForeignKey(Group, verbose_name=_('created for'), null=True, blank=True)
    text = models.TextField(_('content'), blank=True, help_text=_('Use Markdown syntax'))
    text_html = models.TextField(_('html content'), blank=True)

    objects = CommonManager()

    def save(self, *args, **kwargs):
        self.text_html = extend_markdown(self.text)
        self.slug = slugify(self.title)
        super(TextEntry, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = ['title']
