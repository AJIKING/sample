from django.shortcuts import render,redirect
from django.contrib.auth.views import LoginView,PasswordChangeView,LogoutView, PasswordChangeDoneView, PasswordResetView,\
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login as auth_login,get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.template.loader import render_to_string
from django.http import HttpResponseBadRequest
from django.conf import settings
from django.contrib.auth.decorators import login_required
from . import forms
from . import models
from . import mixins
from django.core.mail import send_mail

 # ログインしていないと入れない
User = get_user_model()


class Login(LoginView):
    form_class = forms.LoginForm
    template_name = 'accounts/login.html'


class Logout(LoginRequiredMixin, LogoutView):
    template_name = 'accounts/login.html'


class SignUp(generic.CreateView):
    """account作成"""
    template_name = "accounts/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy('')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        #domeinの取得
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }
        #templateを呼び出す
        subject = render_to_string('mail/create/subject.txt', context)
        message = render_to_string('mail/create/message.txt', context)

        send_mail(subject , message, 'apasn@apasn.com', [user.email], fail_silently=False)

        # user.email_user(subject, message)
        return redirect('accounts:signupdone')

class SignUpDone(generic.TemplateView):
    """ユーザー仮登録"""
    template_name = 'accounts/signupdone.html'

class SignUpComplete(generic.TemplateView):
    """メール内URLアクセス後のユーザー本登録"""

    template_name = 'accounts/signupcomplete.html'
    #settingsインスタンスのactivation_timeout_secondsに時間を設定している
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token,max_age=self.timeout_seconds)
        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    models.UserProfile.objects.create(user=user)
                    auth_login(request, user)
                    #profile編集へ
                    return redirect('accounts:edit')
        return HttpResponseBadRequest()

#ユーザーアカウント情報アップデート
@login_required
def user_edit(request):
  if request.method == 'POST':
    form = forms.UserUpdateForm(request.POST, instance=request.user)
    subform = forms.ProfileUpdateForm(request.POST,request.FILES, instance=request.user.userprofile)

    if all([form.is_valid(), subform.is_valid()]):
      user = form.save()
      profile = subform.save()
      return redirect('person:myaccount', username=request.user)
  else:
    form = forms.UserUpdateForm(instance=request.user)
    subform = forms.ProfileUpdateForm(instance=request.user.userprofile)
  return render(request, 'accounts/accounts_edit.html', {
    'form': form,
    'subform': subform,
  })


class AccountDelete(mixins.OnlyYouMixin,generic.DeleteView):
    template_name = "accounts/delete.html"
    success_url = reverse_lazy("accounts:login")
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'


class PasswordChange(LoginRequiredMixin,PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = forms.MyPasswordChangeForm
    success_url = reverse_lazy('accounts:password_change_done')
    template_name = 'accounts/password_change.html'


class PasswordChangeDone(LoginRequiredMixin,PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'accounts/password_change_done.html'


class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    subject_template_name = 'mail/accounts/password_reset/subject.txt'
    email_template_name = 'mail/accounts/password_reset/message.txt'
    template_name = 'accounts/password_reset_form.html'
    form_class = forms.MyPasswordResetForm
    success_url = reverse_lazy('accounts:password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    form_class = forms.MySetPasswordForm
    success_url = reverse_lazy('accounts:password_reset_complete')
    template_name = 'accounts/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定後ページ"""
    template_name = 'accounts/password_reset_complete.html'

