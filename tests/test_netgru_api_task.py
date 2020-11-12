from django.db import IntegrityError
from rest_framework import status
from rest_framework.test import APITestCase

from netgru_api_task.models import Car, Rating


class AccountTests(APITestCase):
    def test_post_car(self):
        response = self.client.post('/cars',
                                    {'make_name': "HONDA", 'model_name': "Fit"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post('/cars',
                                    {'make_name': "HONDA", 'model_name': "Pilot"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post('/cars',
                                    {'make_name': "HONDA", 'model_name': "Fit"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post('/cars',
                                    {'make_name': "HONDA", 'model_name': "test_wrong_name"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_rate(self):
        response = self.client.post('/rate',
                                    {'make_name': "HONDA", 'model_name': "Fit", "score": 4}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        Car.objects.create(model_name="test_model",make_name="test_make").save()

        response = self.client.post('/rate',
                                    {'make_name': "test_make", 'model_name': "test_model", "score": 3}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post('/rate',
                                    {'make_name': "test_make", 'model_name': "test_model", "score": 0}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post('/rate',
                                    {'make_name': "test_make", 'model_name': "test_model", "score": 6}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_car(self):
        response = self.client.get('/cars', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_popularity(self):
        response = self.client.get('/popular?show=1', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)