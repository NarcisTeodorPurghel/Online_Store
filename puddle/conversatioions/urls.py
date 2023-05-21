from django.urls import path

from . import views

app_name = 'conversatioions'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('<int:primary_key>/', views.detail, name='detail'),
    path('new/<int:item_pk>/', views.new_converstion, name='new'),
]

