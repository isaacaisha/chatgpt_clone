from django.urls import path
from .views import loginPage, logoutUser, registerPage, index, response


urlpatterns = [
    path('', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('register/', registerPage, name='register'),

    path('index', index, name='index'),
    path('index/response', response, name='response')
]
