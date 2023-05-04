from django.urls import path
from secret.apps import SecretConfig
from secret.views import SecretCreateAPIView, SecretDestroyAPIView

app_name = SecretConfig.name

urlpatterns = [
    path('generate/', SecretCreateAPIView.as_view(), name='generate'),
    path('secrets/<str:pk>/', SecretDestroyAPIView.as_view(), name='secrets'),
    ]