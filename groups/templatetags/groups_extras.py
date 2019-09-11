from django import template
from accounts.models import UserBelong

register = template.Library()

#groupの申請確認
@register.filter
def group_petition(user,id):

  if UserBelong.objects.filter(user=user,group=id):
    return True
  else:
    return False
