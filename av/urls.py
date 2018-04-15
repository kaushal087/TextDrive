from django.contrib import admin
from django.urls import path

from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
#from .views import home
from google_auth.views import home
from . import views

urlpatterns = [
    path('login/', auth_views.login, name='login'),
    path('logout/', views.logout_user, name='logout'),
    # path('auth/', include('social_django.urls', namespace='social')),
    path('list/', views.list, name='list'),
    path('save/<file_id>/', views.save, name='update_file'),
    path('save/', views.save, name='create_file'),
    path('editor/<file_id>/', views.editor, name='editor_file'),
    path('editor/', views.editor, name='editor'),
    path('', views.index, name='index'),
]