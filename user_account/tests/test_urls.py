
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from user_account.views import usersignup, activate_account, myaccount_edit


class TestUrls(SimpleTestCase):

    def test_register_user_url_resolves(self):
        url = reverse('register_user')
        self.assertEquals(resolve(url).func, usersignup)

    def test_myaccount_edit_url_resolves(self):
        url = reverse('myaccount_edit')
        self.assertEquals(resolve(url).func, myaccount_edit)

    """ need uid and token to reverse, does not work right now
    def test_activate_url_resolves(self):
        url = reverse('activate')
        self.assertEquals(resolve(url).func, activate_account)
    """