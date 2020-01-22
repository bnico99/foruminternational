from django.test import TestCase, Client
from django.urls import reverse


class TestUserViews(TestCase):

    def setUp(self):
        self.Client = Client()

    """
    def test_usersignup(self):
        response = self.client.get(reverse('register_user'))

        self.assertEqual(response.status_code, 200)
        #self.assertTemplateUsed(response, 'templates/signup.html')
    """
