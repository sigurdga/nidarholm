from haystack.views import SearchView
from django.db.models.query_utils import Q

class RestrictedSearchView(SearchView):
    def __name__(self):
        return "RestrictedSearchView"

    def get_results(self):
        query = super(RestrictedSearchView, self).get_results()
        user = self.request.user
        if user and user.is_authenticated():
            #raise ""
            return query.filter(Q(content=None) | Q(group__user=user))
        else:
            return query.filter(content=None)
