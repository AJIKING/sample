from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import UserRecordContent

# class OnlyRecordEditMixin(UserPassesTestMixin):
#   raise_exception = True
#
#   def test_func(self):
#     user = self.request.user
#     id = self.kwargs['id']
#     print(id)
#     return user.pk == URC.objects.get(id=id).user_id or user.is_superuser


class OnlyRecordEditMixin(LoginRequiredMixin):
  """ユーザーレコードメニュー取得とリクエストユーザー以外のアクセス不可"""
  user_field = 'user'

  def get_queryset(self, *args, **kwargs):
    qs = super().get_queryset(*args, **kwargs)
    if not self.request.user.is_superuser:
      return qs.filter(**{self.user_field: self.request.user})
    return qs
