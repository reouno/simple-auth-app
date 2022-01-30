from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from api_server.apps.custom_accounts import views
from api_server.apps.custom_accounts.apps import CustomAccountsConfig

app_name = CustomAccountsConfig.name

urlpatterns = format_suffix_patterns([
    path('hello/', views.HelloView.as_view(), name='hello'),
])
