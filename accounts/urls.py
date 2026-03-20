from django.urls import path
from . import views

urlpatterns = [
    path('signup/',                           views.signup_view,    name='signup'),
    path('login/',                            views.login_view,     name='login'),
    path('logout/',                           views.logout_view,    name='logout'),
    path('profile/edit/',                     views.edit_profile,   name='edit_profile'),
    path('profile/<str:username>/',           views.profile_view,   name='profile'),
    path('profile/<str:username>/follow/',    views.toggle_follow,  name='toggle_follow'),
    path('profile/<str:username>/followers/', views.followers_list, name='followers'),
    path('profile/<str:username>/following/', views.following_list, name='following'),
    path('search/',                           views.search_view,    name='search'),
]