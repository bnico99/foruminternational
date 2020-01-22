from django.test import TestCase, Client
from django.urls import reverse
from booking.models import Event, Booking, Blocker
import json

class TestViews(TestCase):

    """
    def test_1(self):
        client = Client()

        response = client.get(reverse('post'))

    """