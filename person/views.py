from django.shortcuts import HttpResponse,render_to_response,HttpResponseRedirect
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from accounts.models import User,UserProfile,UserBelong
from django.http import Http404, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from records.models import UserRecordContent

class Home(LoginRequiredMixin,ListView):
    """レコードリスト ホーム"""
    template_name = 'person/home.html'
    paginate_by = 6
    context_object_name = 'records'

    def get_queryset(self):
      user = self.request.user
      try:
        group = UserBelong.objects.get(user=user, approval=1).group
        return UserRecordContent.objects.filter(group=group, )
      except:
        #所属がなければ投稿データのみを取得
        return UserRecordContent.objects.filter(user=self.request.user)


class MyAccount(LoginRequiredMixin,ListView):
    """ログインユーザーアカウント"""
    template_name = 'person/myaccount.html'

    def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      user = self.kwargs.get('username')
      try:#groupに所蔵しているか
        context['groups'] = UserBelong.objects.select_related('user').get(user__username=user).group
      except UserBelong.DoesNotExist:
        pass
      try:#Recordを投稿しているか
        context['count'] = UserRecordContent.objects.select_related('user').filter(user__username=user).count()
      except UserRecordContent.DoesNotExist:
        pass
      context['username'] = user
      context['image'] = UserProfile.objects.select_related('user').get(user__username=user).user_image
      return context

    def get_queryset(self):
      user = self.kwargs.get('username')
      try:
        return UserRecordContent.objects.select_related('user').filter(user__username=user)
      except UserRecordContent.DoesNotExist:
        return



class Menbers(LoginRequiredMixin,ListView):
    """同じグループの所属一覧"""
    template_name = 'person/members.html'
    model = User
    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super(Menbers,self).get_context_data(**kwargs)
        context_data['approval'] = UserProfile.objects.filter(
          user__user_profile__group__userbelong__user=self.request.user.user_id,
          user__user_profile__approval=True
        )
        context_data['unapproved'] = UserProfile.objects.filter(
          user__user_profile__group__userbelong__user=self.request.user.user_id,
          user__user_profile__approval=False
        )

        return context_data

@login_required
def member_approval(request):
    """メンバーの承認ページ"""
    user = request.POST.get('user')
    belong_model = UserBelong.objects.get(user__user_profile__user__username=user)
    belong_model.approval = True
    belong_model.save()
    return HttpResponseRedirect(reverse('person:members'))


class Agreement(TemplateView):
  template_name = 'person/agreement.html'






