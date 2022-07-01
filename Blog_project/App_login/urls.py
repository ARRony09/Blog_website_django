from django.urls import path
from . import views

app_name='App_login'

urlpatterns = [
    path('signup/',views.signup_form,name='signup'),
    path('login/',views.login_form,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('profile/',views.user_profile,name='profile'),
    path('change_profile/',views.change_user_profile,name='change_profile'),
    path('password/',views.change_password,name='password'),
    path('add_pic/',views.add_profile_pic,name='add_profile_pic'),
    path('change_pic/',views.change_picture,name='change_pic'),
]