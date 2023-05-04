from django.urls import path
from secret.apps import SecretConfig
from secret.views import SecretCreateAPIView, SecretRetrieveAPIView

app_name = SecretConfig.name

urlpatterns = [
    path('generate/', SecretCreateAPIView.as_view(), name='generate'),
    path('secrets/<str:pk>/', SecretRetrieveAPIView.as_view(), name='secrets'),
    ]