from django.urls import path, include
from . import views

urlpatterns = [
 path('', views.email_script, name='email_auth'),
#  path('run-script/', views.run_script, name='run_script'),
]
