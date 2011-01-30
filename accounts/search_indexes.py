from haystack.indexes import *
from haystack import site
from django.contrib.auth.models import User

class UserIndex(SearchIndex):
    text = CharField(document=True, use_template=True)

site.register(User, UserIndex)
