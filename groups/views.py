from django.shortcuts import get_object_or_404,render,redirect,HttpResponse,HttpResponseRedirect
from django.http import request
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView
from django.views.generic.edit import ModelFormMixin
from django.urls import reverse_lazy,reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Group
from .forms import GroupRequestForm,GroupCreateForm

from accounts.models import UserBelong
from django.http import JsonResponse
from django.contrib import messages

User = get_user_model()
# Create your views here.

class GroupList(LoginRequiredMixin,ListView,ModelFormMixin):
    """グループの一覧表示"""
    model = Group
    form_class = GroupRequestForm
    success_url = reverse_lazy('groups:group_list')
    template_name = 'groups/group_list.html'
    def get(self, request, *args, **kwargs):
      try:
        UserBelong.objects.get(user=self.request.user,approval=True)
        return HttpResponseRedirect(reverse('person:home'))
      except:
        self.object = None
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
      self.object = None
      self.object_list = self.get_queryset()
      form = self.get_form()
      if form.is_valid():
        return self.form_valid(form)
      else:
        return self.form_invalid(form)

@login_required
@require_http_methods(["POST"])
def GroupRequestAdd(request):
    """所属の申請"""
    group_id = request.POST.get('group')
    approval_data = request.POST.get('approval')
    group_id = Group.objects.get(id=group_id)
    try:
      UserBelong.objects.get(user=request.user.user_id)
      if approval_data == str(1):#既に作成されていた場合には削除する
        UserBelong.objects.get(user=request.user.user_id, group=group_id).delete()
        d = {
          'flag':0
        }
        return JsonResponse(d)
      else:#approvalフラグが書き換えられていた場合作成しない
        d = {
          'flag':2
        }
        return JsonResponse(d)

    except UserBelong.DoesNotExist:#ユーザーがグループへの申請をしていなかった場合
      if approval_data == str(0):
        UserBelong.objects.create(user=request.user,group=group_id)
        d = {
          'flag':1
        }
        return JsonResponse(d)
      else:#approvalフラグが書き換えられていた場合作成しない
        d ={
          'flag':2
        }
        return JsonResponse(d)


class GroupDetail(LoginRequiredMixin,DetailView):
    #TODO:グループの詳細 未実装
    model = Group
    template_name = 'groups/group_detail.html'

class GroupCreate(LoginRequiredMixin,CreateView):
    """group作成"""
    model = Group
    template_name = 'groups/group_create.html'
    form_class = GroupCreateForm
    success_url = reverse_lazy('person:home')


    def form_valid(self, form):
      try:
        #ユーザーがグループに所属確認
        group_serch = UserBelong.objects.get(user=self.request.user.user_id)
        messages.info(self.request, 'グループ申請中は作成できません。')
        return HttpResponseRedirect(reverse('groups:group_create'))
      except UserBelong.DoesNotExist:
        group_create = form.save()
        username = User.objects.get(username=self.request.user)
        # 作成と同時に所属する
        UserBelong.objects.create(user=username, group=form.instance, approval=True)
        return super().form_valid(form)



