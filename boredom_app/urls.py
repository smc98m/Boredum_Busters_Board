from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('register_user', views.register_user),
    path('register', views.register),
    path('choiceBoard', views.choiceBoard),
    path('admin_edits', views.admin_edits),
    path('createActivity/<int:id>', views.createActivity),
    path('createReward/<int:id>', views.createReward),
    path('delete/<int:id>', views.delete),
    path('completed_activity/<int:id>', views.completed_activity),
    path('logout', views.logout),
]