from django.urls import path

from . import views

app_name = 'oauth'

urlpatterns = [
    path('google', views.google_oauth_redirect, name='google_oauth_redirect'),
    path('', views.index, name='index'),
    path('page', views.page, name='page')

]

