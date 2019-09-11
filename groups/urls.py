from django.urls import path
from . import views


app_name = 'groups'

urlpatterns = [
    path('',views.GroupList.as_view(),name='group_list'),#部活動メンバーの一覧表示
    path('ajax_post_add/',views.GroupRequestAdd,name='ajax_post_add'),
    path('<str:group_id>/request/',views.GroupDetail.as_view(),name='group_detail'),
    path('create/',views.GroupCreate.as_view(),name='group_create')
]
