class LazyOrganization(object):
    def __get__(self, request, obj_type=None):
        if not hasattr(request, '_cached_organization'):
            from organization.models import get_organization
            request._cached_organization = get_organization(request)
        return request._cached_organization

class OrganizationMiddleware(object):
    def process_request(self, request):
        request.__class__.organization = LazyOrganization()
        return None

