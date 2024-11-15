from django.urls import path
from .views import registerPage, loginPage, logoutUser, index, response, superuser_page


urlpatterns = [
    path('register/', registerPage, name='register'),
    path('', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),

    path('index', index, name='index'),
    path('index/response', response, name='response'),

    path('superuser/', superuser_page, name='superuser_page'),
]
