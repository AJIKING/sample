from django import forms
from person import mixins
from accounts.models import UserBelong
from .models import Group

class GroupRequestForm(mixins.BaseModelForm):
    """Group 所属フォーム"""
    class Meta:
        model = UserBelong
        fields = ('group',)


class GroupCreateForm(mixins.BaseModelForm):
    """Group 作成フォーム"""
    class Meta:
      model = Group
      fields = ('group_id','group_name','group_image',)
      labels = {'group_image':'画像'}


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'






