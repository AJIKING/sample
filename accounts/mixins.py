from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth import get_user_model


User = get_user_model()


class OnlyYouMixin(UserPassesTestMixin):
  """ログインユーザーとスーパーユーザーのみアクセス権限"""
  raise_exception = True

  def test_func(self):
    user = self.request.user
    return user.username == self.kwargs['username'] or user.is_superuser

class ModelFormWithFormSetMixin:
  """inlineform用 データ検証"""
  def __init__(self, *args, **kwargs):
    super(ModelFormWithFormSetMixin, self).__init__(*args, **kwargs)
    self.formset = self.formset_class(
      instance=self.instance,
      data=self.data if self.is_bound else None,
    )

  def is_valid(self):
    return super(ModelFormWithFormSetMixin, self).is_valid() and self.formset.is_valid()

  def save(self, commit=True):
    saved_instance = super(ModelFormWithFormSetMixin, self).save(commit)
    self.formset.save(commit)
    return saved_instance



