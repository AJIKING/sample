from django import forms

#forms.label_tagの:を消す
class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
      kwargs.setdefault('label_suffix', '')
      super(BaseForm, self).__init__(*args, **kwargs)

#forms.label_tagの:を消す
class BaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
      kwargs.setdefault('label_suffix', '')
      super(BaseModelForm, self).__init__(*args, **kwargs)

