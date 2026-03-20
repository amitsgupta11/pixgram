from django.urls import path
from . import views

urlpatterns = [
    # Posts
    path('create/',           views.create_post,       name='create_post'),
    path('<int:pk>/',         views.post_detail,       name='post_detail'),
    path('<int:pk>/edit/',    views.edit_post,         name='edit_post'),
    path('<int:pk>/delete/',  views.delete_post,       name='delete_post'),
    path('<int:pk>/like/',    views.toggle_like,       name='toggle_like'),
    path('<int:pk>/comment/', views.add_comment,       name='add_comment'),
    path('<int:pk>/save/',    views.toggle_save,       name='toggle_save'),
    path('<int:pk>/share/',   views.share_post,        name='share_post'),

    # Saved & Notifications & Explore
    path('saved/',            views.saved_posts,        name='saved_posts'),
    path('notifications/',    views.notifications_view, name='notifications'),
    path('explore/',          views.explore_view,       name='explore'),

    # Stories
    path('story/create/',          views.create_story, name='create_story'),
    path('story/<int:pk>/',        views.view_story,   name='view_story'),
    path('story/<int:pk>/delete/', views.delete_story, name='delete_story'),
    path('story/mine/',            views.my_stories,   name='my_stories'),

    # Direct Messages
    path('dm/',                  views.dm_inbox,        name='dm_inbox'),
    path('dm/new/',              views.dm_new,          name='dm_new'),
    path('dm/<str:username>/',   views.dm_conversation, name='dm_conversation'),
]