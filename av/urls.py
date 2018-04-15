from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('login/', auth_views.login, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('list/', views.list, name='list'),
    path('save/<file_id>/', views.save, name='update_file'),
    path('create/', views.create, name='create_file'),
    path('editor/<file_id>/', views.editor, name='editor_file'),
    path('editor/', views.editor, name='editor'),
    path('', views.index, name='index'),
]
