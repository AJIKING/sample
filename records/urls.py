from django.urls import path,include
from . import views


app_name = 'records'

urlpatterns = [
    path('recordcreate/',views.RecordCreate.as_view(),name='recordcreate'),
    path('title_create/',views.title_create,name='title_create'),
    path('<id>/', views.RcordDetail.as_view(), name='record_detail'),
    path('<id>/edit/', views.RecordDetailEdit.as_view(), name='record_detail_edit'),
    path('<id>/delete/',views.RecordDetailDelete.as_view(),name='record_detail_delete'),

]
