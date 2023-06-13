from django.urls import path
from job.views import *

urlpatterns = [
    path('',JobView.as_view(),name='job'),
    path('<int:id>/',JobView.as_view(),name='get_job'),
    path('application/',JobApplicationView.as_view(),name='job_application'),
    path('application/history/<int:id>/',JobApplicationView.as_view(),name='job_application'),
]