from django.urls import path
from . import views

urlpatterns = [
    path('register/',               views.register,        name='register'),
    path('login/',                  views.login_view,      name='login'),
    path('logout/',                 views.logout_view,     name='logout'),
    path('profile/<str:username>/', views.profile,         name='profile'),
    path('profile/<str:username>/edit/',           views.edit_profile,    name='edit_profile'),
    path('search/',                 views.search_users,    name='search_users'),
    path('suggested/',              views.suggested_users, name='suggested_users'),
]