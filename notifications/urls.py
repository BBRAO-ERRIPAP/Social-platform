from django.urls import path
from . import views

urlpatterns = [
    path('',       views.notifications_list, name='notifications_list'),
    path('read/',  views.mark_all_read,      name='mark_all_read'),
    path('count/', views.unread_count,       name='unread_count'),
]