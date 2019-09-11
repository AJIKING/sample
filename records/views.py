from django.views.generic import CreateView,UpdateView,TemplateView,DetailView,DeleteView
from django.urls import reverse_lazy,reverse
from django.shortcuts import get_object_or_404,render,redirect,HttpResponse,HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from . import models
from . import forms
from accounts.models import UserBelong
from django.contrib import messages
from . import mixins


User = get_user_model()

class RecordCreate(LoginRequiredMixin,CreateView):
    """レコード作成"""
    model = models.UserRecordContent
    form_class = forms.RecordCreateForm
    template_name = 'records/user_record_create.html'
    success_url = reverse_lazy('person:home')

    def get_context_data(self, **kwargs):
      context_data = super(RecordCreate, self).get_context_data(**kwargs)
      context_data['title_create'] = forms.RecordTitleCreateForm

      return context_data

    def get_form_kwargs(self):
      kwargs = super(RecordCreate, self).get_form_kwargs()
      kwargs['user'] = self.request.user
      return kwargs

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        try:
          form.instance.group = UserBelong.objects.get(user=user).group
        except:
          pass
        return super().form_valid(form)
@login_required
@require_http_methods(["POST"])
def title_create(request):
    """レコードタイトル作成"""
    title_name = request.POST.get('user_record_title_name')
    models.UserRecordTitle.objects.create(user=request.user,user_record_title_name=title_name)
    return HttpResponseRedirect(reverse('records:recordcreate'))


class RcordDetail(LoginRequiredMixin,DetailView):
    """レコード詳細"""
    template_name = 'records/user_record_detail.html'
    model = models.UserRecordContent
    pk_url_kwarg = 'id'

class RecordDetailEdit(mixins.OnlyRecordEditMixin,UpdateView):
    """レコード編集"""
    template_name = 'records/user_record_edit.html'
    model = models.UserRecordContent
    pk_url_kwarg = 'id'
    form_class = forms.RecordDetailEditForm
    success_url = reverse_lazy('person:home')

    def get_form_kwargs(self):
      #formにuser情報を渡す
      kwargs = super(RecordDetailEdit, self).get_form_kwargs()
      kwargs['user'] = self.request.user
      return kwargs

    def form_valid(self, form):
      #削除されていた場合はデフォルトを適用する
      if not form.instance.user_record_image:
        form.instance.user_record_image = 'records/default.jpg'
      return super().form_valid(form)

class RecordDetailDelete(LoginRequiredMixin,DeleteView):
    """レコード削除"""
    template_name = 'records/user_record_delete.html'
    model = models.UserRecordContent
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('person:home')
