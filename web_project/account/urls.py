from django.urls import include, path
from . import views


app_name = 'account'


urlpatterns = [
    # accounts/register/
    path('register/', views.register, name='register'),
]
