from django.test import TestCase, RequestFactory
from rest_framework.test import APITestCase, APIRequestFactory
from .models import Category
from .serializers import CategorySerializer
from django.urls import reverse
from .views import CatDetailView
import json
from operator import itemgetter

class CatAPITestCase(APITestCase):
    url = reverse("testovoe:list")
    def setUp(self):
        self.category1 = Category.objects.create(name='CategoryTest 1')
        self.category2 = Category.objects.create(
            name='CategoryTest 1.1', parent=self.category1)
        self.category3 = Category.objects.create(
            name='CategoryTest 1.1.1', parent=self.category2)
        self.category4 = Category.objects.create(
            name='CategoryTest 1.2', parent=self.category1)

    def test_get_valid_category(self):
        response = self.client.get(self.url)
        data = list(json.loads(response.content))
        self.assertEqual(200, response.status_code)
        self.assertTrue(self.category1.name in map(itemgetter('name'), data))
        self.assertTrue(self.category2.name in map(itemgetter('name'), data))
        self.assertTrue(self.category3.name in map(itemgetter('name'), data))
        self.assertTrue(self.category4.name in map(itemgetter('name'), data))

        

class CatAPIPostTestCase(APITestCase):
    url = reverse("testovoe:list")

    def setUp(self):
        self.data_send = {
            "name": "Category 1",
            "children": [
                {
                    "name": "Category 1.1",
                    "children": [
                        {
                            "name": "Category 1.1.1",
                            "children": [
                                {
                                    "name": "Category 1.1.1.1"
                                },
                                {
                                    "name": "Category 1.1.1.2"
                                },
                                {
                                    "name": "Category 1.1.1.3"
                                }
                            ]
                        },
                        {
                            "name": "Category 1.1.2",
                            "children": [
                                {
                                    "name": "Category 1.1.2.1"
                                },
                                {
                                    "name": "Category 1.1.2.2"
                                },
                                {
                                    "name": "Category 1.1.2.3"
                                }
                            ]
                        }
                    ]
                },
                {
                    "name": "Category 1.2",
                    "children": [
                        {
                            "name": "Category 1.2.1"
                        },
                        {
                            "name": "Category 1.2.2",
                            "children": [
                                {
                                    "name": "Category 1.2.2.1"
                                },
                                {
                                    "name": "Category 1.2.2.2"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    def test_post_category(self):
        response = self.client.post(self.url, json.dumps(
            self.data_send), content_type='application/json')
        self.assertEqual(201, response.status_code)
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertTrue(len(json.loads(response.content))
                        == Category.objects.count())