from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password, check_password

import pytz
from rest_framework import generics, status
from rest_framework.response import Response
from config import settings

from secret.models import Secret
from secret.serializers import SecretSerializer
from secret.services import encrypt, decrypt
from secret.tasks import delete_after_view


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


class SecretRetrieveAPIView(generics.RetrieveAPIView):
    """
    Controller for read a secret
    """

    serializer_class = SecretSerializer
    queryset = Secret.objects.all()

    def get(self, request, *args, **kwargs):
        """
        The method must accept the required parameter "key"
        """
        key = request.data.get('key')
        if key is None:
            raise AttributeError('The "key" attribute must be passed')
        return self.retrieve(request, key, *args, **kwargs)

    def retrieve(self, request, key=None, *args, **kwargs):
        """
        The method compares the "key" parameter, returns the decrypted phrase and deletes it from the database
        """

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if key:
            if check_password(key, serializer.data.get('key')):
                answer = Response({'answer': 'Confirmed',
                                  'phrases': decrypt(serializer.data.get('phrases'))})
                delete_after_view.delay(serializer.data.get('uuid'))
                return answer
            return Response({'answer': 'The keyword does not match',
                             'phrases': None}, status=status.HTTP_400_BAD_REQUEST)






