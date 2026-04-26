from django.urls import path
from . import views

urlpatterns = [
    path('posts/',                        views.PostListCreateView.as_view(),   name='api_posts'),
    path('posts/<int:pk>/',               views.PostDetailView.as_view(),       name='api_post_detail'),
    path('posts/<int:post_id>/comments/', views.CommentListCreateView.as_view(),name='api_comments'),
    path('posts/<int:pk>/like/',          views.api_toggle_like,                name='api_toggle_like'),
    path('users/',                        views.UserListView.as_view(),          name='api_users'),
    path('users/<str:username>/',         views.UserDetailView.as_view(),        name='api_user_detail'),
    path('users/<str:username>/follow/',  views.api_toggle_follow,               name='api_toggle_follow'),
]