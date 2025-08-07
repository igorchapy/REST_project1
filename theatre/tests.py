from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from theatre.models import Play


class PlayAPITestCase(APITestCase):
    def setUp(self):
        self.play = Play.objects.create(title="Macbeth", description="Tragedy")
        self.url_list = reverse('play-list')
        self.url_detail = reverse('play-detail', kwargs={'pk': self.play.pk})

    def test_get_all_plays(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_play(self):
        data = {"title": "Hamlet", "description": "Another Shakespeare play"}
        response = self.client.post(self.url_list, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_play(self):
        updated_data = {"title": "Macbeth Updated", "description": "Updated desc"}
        response = self.client.put(self.url_detail, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Macbeth Updated")

    def test_delete_play(self):
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
