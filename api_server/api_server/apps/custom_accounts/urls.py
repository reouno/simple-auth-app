from django.urls import path

from api_server.apps.custom_accounts import views
from api_server.apps.custom_accounts.apps import CustomAccountsConfig

app_name = CustomAccountsConfig.name

urlpatterns = [
    path('hello/', views.HelloView.as_view(), name='hello'),
]
