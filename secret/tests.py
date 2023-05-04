from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from secret.models import Secret


class SecretTestCase(APITestCase):

    def test_secret_create(self):

        response = self.client.post(reverse('secret:generate'),
                                    {
                                        "key": "key_phrase",
                                        "phrases": "secret secret",
                                        "lifetime": "5 minutes"
                                    }
                                    )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_secret_destroy(self):

        self.test_secret_create()
        secret_uuid = Secret.objects.first().uuid
        response = self.client.delete(reverse('secret:secrets', args=[secret_uuid]), data={'key': "key_phrase"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('phrases'), "secret secret")

    def test_secret_destroy_second_response(self):
        self.test_secret_create()
        secret_uuid = Secret.objects.first().uuid
        self.client.delete(reverse('secret:secrets', args=[secret_uuid]), data={'key': "key_phrase"})
        response = self.client.delete(reverse('secret:secrets', args=[secret_uuid]), data={'key': "key_phrase"})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_secret_destroy_false(self):
        self.test_secret_create()
        secret_uuid = Secret.objects.first().uuid
        response = self.client.delete(reverse('secret:secrets', args=[secret_uuid]), data={'key': "key"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'answer': 'The keyword does not match', 'phrases': None})
