"""
URL configuration for privetproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from privet import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/student/profile/<int:pk>/', views.StudentProfileView.as_view()),
    path('api/v1/buddy/profile/<int:pk>/', views.BuddyProfileView.as_view()),

    path('api/v1/signup/student/', views.StudentSignupView.as_view()),
    path('api/v1/confirm/student/', views.StudentConfirmationView.as_view()),
    path('api/v1/signup/buddy/', views.BuddySignupView.as_view()),
    path('api/v1/login/', views.CustomAuthToken.as_view()),
    path('api/v1/logout/', views.LogoutView.as_view()),

    path('api/v1/student/arrival-booking/<int:pk>/', views.ArrivalBookingView.as_view()),
    path('api/v1/student/arrival-booking/add-student/', views.ArrivalOtherStudentView.as_view()),

    path('api/v1/buddy/arrivals/', views.AllArrivalBookingsView.as_view()),
    path('api/v1/buddy/arrivals/<int:pk>/', views.DefiniteArrivalBookingView.as_view()),

    path('api/v1/buddy/add-arrival/', views.AddArrivalToBuddy.as_view()),
    path('api/v1/buddy/buddy-arrivals/<int:user>/', views.BuddyArrivalsView.as_view()),
    path('api/v1/buddy/student/<int:pk>/', views.StudentProfileForBuddyView.as_view()),
    path('api/v1/buddy/buddy-students/<int:pk>/', views.BuddyStudentsView.as_view()),

    path('api/v1/teamlead/add-buddy-to-arrival/', views.AddBuddyToArrivalView.as_view()),
    path('api/v1/teamlead/delete-arrival/', views.DeleteBuddyArrivalView.as_view()),
]