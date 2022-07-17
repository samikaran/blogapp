from django.urls import path, re_path
from blog import views

urlpatterns = [
    path('', views.blogs, name='blogs'),
    path('post/<str:slug>/', views.blogDetail, name='blogDetail'),
    # path(r'^post/(?P<slug>[^\.]+)/$', views.blogDetail, name='blogDetail'),
    path('upload/', views.uploadBlog, name='uploadBlog'),
]
