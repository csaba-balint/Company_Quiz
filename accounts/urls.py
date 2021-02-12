from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginPage, name="login"),
    # path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('user/<str:pk>/', views.userPage, name="userPage"),
    path('addQuestion/<str:pk>/', views.addQuestion, name="addQuestion"),
    path('candidateLogin/<str:pk>/<str:token>', views.candidateLogin, name="candidateLogin"),
    path('candidatePage/<str:pk_comp>/<str:pk_cand>/<str:pk_quest>', views.candidatePage, name="candidatePage"),
    path('invite/<str:pk>/', views.invite, name="invite"),

]