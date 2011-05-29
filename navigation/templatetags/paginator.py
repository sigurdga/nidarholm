from django import template

register = template.Library()

def paginator(context, adjacent_pages=4):
    """
    To be used in conjunction with the object_list generic view.

    Adds pagination context variables for use in displaying first, adjacent and
    last page links in addition to those created by the object_list generic
    view.
    """
    paginator = context["paginator"]
    page_obj = context["page_obj"]
    page_numbers = [n for n in range(context["page"] - adjacent_pages, context["page"] + adjacent_pages + 1) if n > 0 and n <= paginator.num_pages]
    return {
        "hits": paginator.count,
        "page": context["page"],
        "pages": paginator.num_pages,
        "page_numbers": page_numbers,
        "next": page_obj.next_page_number,
        "previous": page_obj.previous_page_number,
        "has_next": page_obj.has_next,
        "has_previous": page_obj.has_previous,
        "show_first": 1 not in page_numbers,
        "show_last": paginator.num_pages not in page_numbers,
    }

register.inclusion_tag("navigation/paginator.html", takes_context=True)(paginator)
