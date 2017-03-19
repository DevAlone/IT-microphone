from django import template

register = template.Library()


@register.filter(name='is_user_subscribed_to_event')
def is_user_subscribed_to_event(user, event):
    return event.subscribers.filter(pk=user.pk).exists()
