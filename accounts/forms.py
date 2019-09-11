from django.contrib.auth.forms import UserCreationForm,AuthenticationForm, PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django import forms
from django.contrib.auth import get_user_model
from . import models
from person.mixins import BaseModelForm,BaseForm
from django.utils.translation import gettext_lazy as _


User = get_user_model()

class SignUpForm(BaseForm,UserCreationForm):
    """ユーザー登録用フォーム"""

    class Meta:
        model = User
        fields = ('email','username')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email


class ProfileUpdateForm(BaseModelForm):
    """ProfileModelアップデートフォーム"""
    class Meta:
        model = models.UserProfile
        fields = ('first_name','last_name','birthday','user_image',)

        widgets = {
          'first_name': forms.TextInput(attrs={'class': 'form-control'}),
          'last_name': forms.TextInput(attrs={'class': 'form-control'}),
          'birthday': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
          'user_image': _('プロフィール画像')
        }


class UserUpdateForm(BaseModelForm):
    #Userモデルにprofileモデルを入れる
    # formset_class = ProfileFormSet
    class Meta:
        model = User
        fields = ('username',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class ProfileForm(BaseModelForm):

    class Meta:
        model = models.UserProfile
        fields = ('first_name','last_name','birthday',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['birthday'].widget = forms.SelectDateWidget(years=[x for x in range(1990, 2030)]) # 引数にattrs={'class': 'form-control'}も可能

class LoginForm(BaseForm,AuthenticationForm):
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      for field in self.fields.values():
        field.widget.attrs['class'] = 'form-control'
        field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる


class MyPasswordChangeForm(BaseForm,PasswordChangeForm):
    """パスワード変更フォーム"""

    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      for field in self.fields.values():
        field.widget.attrs['class'] = 'form-control'
        field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる

class MyPasswordResetForm(BaseForm,PasswordResetForm):
    """パスワード忘れたときのフォーム"""

    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      for field in self.fields.values():
        field.widget.attrs['class'] = 'form-control'


class MySetPasswordForm(BaseForm,SetPasswordForm):
    """パスワード再設定用フォーム(パスワード忘れて再設定)"""

    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      for field in self.fields.values():
        field.widget.attrs['class'] = 'form-control'

