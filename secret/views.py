from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password, check_password

import pytz
from rest_framework import generics, status
from rest_framework.response import Response
from config import settings

from secret.models import Secret
from secret.serializers import SecretSerializer
from secret.services import encrypt, decrypt


class SecretCreateAPIView(generics.CreateAPIView):
    """
    Controller for creating a secret
    """
    serializer_class = SecretSerializer

    def create(self, request, *args, **kwargs):
        """
        The method has been redefined to encrypt data (key and phrases) and return a custom URL
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        key = make_password(serializer.validated_data.get("key"))
        phrases = encrypt(serializer.validated_data.get("phrases"))
        serializer.validated_data["key"] = key
        serializer.validated_data["phrases"] = phrases

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        url = f'{settings.BASE_URL}/secrets/{serializer.data.get("uuid")}/'

        return Response({'url': url}, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        """
        Save delete_data
        """

        lifetime_dict = {'7 days': timedelta(days=7),
                    '3 days': timedelta(days=3),
                    '1 day': timedelta(days=1),
                    '12 hours': timedelta(hours=12),
                    '4 hours': timedelta(hours=4),
                    '1 hour': timedelta(hours=1),
                    '30 minutes': timedelta(minutes=30),
                    '5 minutes': timedelta(minutes=5)
                         }
        lifetime = '7 days'
        if serializer.validated_data.get('lifetime'):
            lifetime = serializer.validated_data.get('lifetime')
        delete_data = datetime.now().astimezone(pytz.timezone(settings.TIME_ZONE)) + lifetime_dict[lifetime]
        serializer.save(delete_data=delete_data)


class SecretDestroyAPIView(generics.DestroyAPIView):
    """
    Controller for read a secret
    """

    serializer_class = SecretSerializer
    queryset = Secret.objects.all()

    def delete(self, request, *args, **kwargs):
        """
        The method must accept the required parameter "key"
        """
        key = request.data.get('key')
        if key is None:
            raise AttributeError('The "key" attribute must be passed')
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.data.get('key'):
            if check_password(request.data.get('key'), instance.key):
                answer = Response({'answer': 'Confirmed',
                                  'phrases': decrypt(instance.phrases)})
                self.perform_destroy(instance)
                return answer

            return Response({'answer': 'The keyword does not match', 'phrases': None},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({'answer': 'The "key" argument is omitted', 'phrases': None},
                            status=status.HTTP_400_BAD_REQUEST)







