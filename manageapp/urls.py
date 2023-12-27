from django.urls import path
from manageapp import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('user_login/', views.user_login, name='userlogin'),
    path('user_signup', views.user_signup, name='usersignup'),
    path('user_logout/', views.user_logout, name='userlogout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    
]
