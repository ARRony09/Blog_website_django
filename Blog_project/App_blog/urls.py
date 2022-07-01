from django.urls import path
from . import views

app_name="App_blog"

urlpatterns = [
    path('',views.BlogList.as_view(),name='blog_list'),
    path('write/',views.CreateBlog.as_view(),name='create_blog'),
    path('details/<str:slug>',views.blog_details,name='blog_details'),
    path('liked/<pk>/',views.like_post,name='liked_post'),
    path('unliked/<pk>/',views.unliked_post,name='unliked_post'),
    path('my-blog/',views.MyBLog.as_view(),name='my_blog'),
    path('edit-blog/<pk>/',views.EditBlog.as_view(),name='edit_blog'),
]