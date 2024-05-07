from django.urls import path
from . import views
from social_app.views import *


urlpatterns = [
    path("", views.home, name='home'),
    path("login/", views.login_user, name='login_user'),
    path("logout/", views.logout_user, name="logout_user"),
    path("signup/", views.signup, name="signup"),
    path("addnewplace/", views.add_new_place, name="add_new_place"),
    path("post/<str:place_id>/", create_post, name="create_post"),
    path("post/like/<pk>/", like_post, name="like-post"),
    path("comment/like/<pk>/", like_comment, name="like-comment"),
    path("feed/", feed, name="feed"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("profilesettings/", views.profile_settings, name="profile_settings"),
    path("postcontent/<str:post_id>/", post_content, name="post_content"),
    path("event/<str:place_id>/", create_event, name="create_event"),
    path("show_event/", show_event, name="show_event"),
    path('commentsent/<int:post_id>/', comment_sent, name='comment-sent'), 
    path('comment/delete/<int:comment_id>/', comment_delete, name='comment-delete'),
    path('reply-sent/<int:comment_id>/', reply_sent, name='reply-sent'),
    path('reply/delete/<int:reply_id>/', reply_delete, name='reply-delete'),
    
    
]