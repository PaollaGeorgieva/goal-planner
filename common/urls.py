from django.urls import path, include
from common import views

urlpatterns = [
    path('', views.LandingPageView.as_view(), name='landing-page'),
    path('home/', views.HomePageView.as_view(), name='home'),
]