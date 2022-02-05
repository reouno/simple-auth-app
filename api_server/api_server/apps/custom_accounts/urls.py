from django.urls import path

from api_server.apps.custom_accounts import views
from api_server.apps.custom_accounts.apps import CustomAccountsConfig

app_name = CustomAccountsConfig.name

urlpatterns = [
    path('set-csrf/', views.SetCsrf.as_view(), name='set-csrf'),
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('current/', views.UserViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
    }), name='current'),
]
