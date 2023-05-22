from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def get_newest_offers(all_offers):
    offers = all_offers.order_by('created_data')

    return mark_safe(offers[:1])

