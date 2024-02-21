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
    path("feed/", feed, name="feed"),
    path("test/", views.test, name="test"),
    path("profilesettings/", views.profile_settings, name="profile_settings"),
    path("postcontent/<str:post_id>/", post_content, name="post_content")

    
]