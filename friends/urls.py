from django.urls import path
from . import views

urlpatterns = [
    path('follow/<str:username>/',             views.toggle_follow,          name='toggle_follow'),
    path('request/<str:username>/',            views.send_friend_request,    name='send_friend_request'),
    path('request/<int:request_id>/respond/',  views.respond_friend_request, name='respond_friend_request'),
    path('followers/<str:username>/',          views.followers_list,         name='followers_list'),
    path('following/<str:username>/',          views.following_list,         name='following_list'),
    path('list/',                              views.friends_list,           name='friends_list'),
]