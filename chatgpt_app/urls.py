from django.urls import path
from .views import registerPage, vipPage, registerVipUser, loginVipPage, loginPage, logoutUser, index, response


urlpatterns = [
    path('register/', registerPage, name='register'),
    path('', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),

    path('index', index, name='index'),
    path('index/response', response, name='response'),

    path('register_vip/', registerVipUser, name='register_vip'),
    path('login_vip/', loginVipPage, name='login_vip'),
    path('vip_user/', vipPage, name='vip_user'),
]
