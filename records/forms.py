from django import forms
from . import models
from person.mixins import BaseModelForm
import bootstrap_datepicker_plus as datetimepicker
from django.utils.translation import gettext_lazy as _


class RecordTitleCreateForm(BaseModelForm):
    class Meta:
        model = models.UserRecordTitle
        fields = ('user_record_title',)
        widgets = {
            'user_record_title': forms.TextInput(attrs={'class': 'form-control'}),}


class RecordCreateForm(BaseModelForm):
    class Meta:
        model = models.UserRecordContent
        fields = ('user_record_title','user_record_image','user_record_content',
                  'user_record_elapsed_time','user_record_time',)
        widgets = {
            'user_record_content': forms.TextInput(attrs={'class': 'form-control'}),}
        labels = {
          'user_record_title': _('タイトル'),
          'user_record_content': _('内容・ひとこと'),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(RecordCreateForm,self).__init__(*args, **kwargs)
        self.fields['user_record_title'].queryset = models.UserRecordTitle.objects.filter(user=user)
        self.fields['user_record_title'].widget.attrs = {'class':'form-control'}
        self.fields['user_record_elapsed_time'].widget = datetimepicker.TimePickerInput(
                format='%H:%M',
                attrs={'readonly': 'true'},
                options={
                    'locale': 'ja',
                    'ignoreReadonly': True,
                    'allowInputToggle': True,
                })
        self.fields['user_record_time'].widget = datetimepicker.DateTimePickerInput(
                format='%Y-%m-%d %H:%M',
                attrs={'readonly': 'true'},
                options={
                    'locale': 'ja',
                    'dayViewHeaderFormat': 'YYYY年 MMMM',
                    'ignoreReadonly': True,
                    'allowInputToggle': True,
                }
            )

class RecordDetailEditForm(BaseModelForm):
    class Meta:
        model = models.UserRecordContent
        fields = ('user_record_image','user_record_title','user_record_content',
                  'user_record_elapsed_time','user_record_time')
        widgets = {
            'user_record_content': forms.TextInput(attrs={'class': 'form-control'}), }
        labels = {
          'user_record_title': _('タイトル'),
        }


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(RecordDetailEditForm, self).__init__(*args, **kwargs)
        self.fields['user_record_title'].queryset = models.UserRecordTitle.objects.filter(user=user)
        self.fields['user_record_title'].widget.attrs = {'class':'form-control'}
        self.fields['user_record_elapsed_time'].widget = datetimepicker.TimePickerInput(
            format='%H:%M',
            attrs={'readonly': 'true'},
            options={
                'locale': 'ja',
                'ignoreReadonly': True,
                'allowInputToggle': True,
              })
        self.fields['user_record_time'].widget = datetimepicker.DateTimePickerInput(
            format='%Y-%m-%d %H:%M',
            attrs={'readonly': 'true'},
            options={
                'locale': 'ja',
                'dayViewHeaderFormat': 'YYYY年 MMMM',
                'ignoreReadonly': True,
                'allowInputToggle': True,
            })

