from django.urls import path
from website import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('login', views.frontLogin, name='login'),
    path('signup', views.frontSignup, name='signup'),
    path('logout', views.frontLogout, name='logout'),
    path('search', views.frontSearch, name='search'),
]
