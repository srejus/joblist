from django.urls import path
from accounts.views import *

urlpatterns = [
    path('signup/',SignupView.as_view(),name='signup'),
    path('user/<int:id>/',SignupView.as_view(),name='view_user'),
    path('company/',CompanyView.as_view(),name='company'),
    path('company/<int:id>/',CompanyView.as_view(),name='view_company'),
]