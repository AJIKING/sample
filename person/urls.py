from django.urls import path,include
from . import views


app_name = 'person'

urlpatterns = [
    path('',views.Home.as_view(),name='home'),#部活動メンバーの一覧表示
    path('<slug:username>/myaccount/', views.MyAccount.as_view(), name='myaccount'),  # 該当アカウント
    path('members/', views.Menbers.as_view(), name='members'),  # members
    path('members/approval/',views.member_approval,name='member_approval'),
    path('agreement/',views.Agreement.as_view(),name='agreement'),
]
