from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/',views.Logout.as_view(),name='logout'),
    path('signup/',views.SignUp.as_view(),name='signup'),
    path('signupdone/',views.SignUpDone.as_view(),name='signupdone'),
    path('signupcomplete/<token>/',views.SignUpComplete.as_view(),name='signupcomplete'),
    path('edit/', views.user_edit, name='edit'),
    path('delete/<slug:username>/', views.AccountDelete.as_view(), name='delete'),
    path('password/change/', views.PasswordChange.as_view(), name='password_change'),
    path('password/change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
]
