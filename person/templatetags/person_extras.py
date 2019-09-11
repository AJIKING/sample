from django import template
from accounts.models import UserBelong

register = template.Library()

#groupに所属しているか
@register.filter
def belong_judgment(user):

  if UserBelong.objects.filter(user=user,approval=True):
    return True
  else:
    return False
