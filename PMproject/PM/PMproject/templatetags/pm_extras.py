from django import template
from ..models import Like

register = template.Library()


@register.filter
def like_filter(user, photo):
    return Like.objects.filter(photo=photo, user=user)


