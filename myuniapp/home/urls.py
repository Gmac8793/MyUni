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
    path("reply/like/<pk>/", like_reply, name="like-reply"),
    path("feed/", feed, name="feed"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("profilesettings/", views.profile_settings, name="profile_settings"),
    path("postcontent/<str:post_id>/", post_content, name="post_content"),
    path("event/<str:place_id>/", create_event, name="create_event"),
    path("event_details/<pk>/", event_details, name="event_details"),
    path("event_edit/<pk>/", event_edit, name="event_edit"),
    path("show_event/", show_event, name="show_event"),
    path('commentsent/<int:post_id>/', comment_sent, name='comment-sent'), 
    path('comment/delete/<int:comment_id>/', comment_delete, name='comment-delete'),
    path('reply-sent/<int:comment_id>/', reply_sent, name='reply-sent'),
    path('replyform/<pk>/', reply_form, name="reply-form"),
    path('reply/delete/<int:reply_id>/', reply_delete, name='reply-delete'),
    path('calendar/', event_calendar, name='event_calendar'),
    path('event/delete/<int:event_id>/', event_delete, name='event-delete'),
    path('all_events/', all_events, name='all_events'),
    path('event_from_calendar/', event_from_calendar, name='event_from_calendar'),
    path('add_event_member/<int:event_id>/', add_event_member, name='add_event_member'),
    path('notifications/', notifications, name='notifications'),
    path('notifications/read/', mark_notifications_as_read, name='mark_notifications_as_read'),
    path('event/<int:event_id>/remove_member/<int:member_id>/', remove_member, name='remove_member'),
]