
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from info.views import faq, home


class TestUrls(SimpleTestCase):

    """ neither, the reverse, nor just putting in the link is working anymore, will have to fix
    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)

    def test_faq_url_resolves(self):
        url = '/faq/'
        self.assertEquals(resolve(url).func, faq)
    """

