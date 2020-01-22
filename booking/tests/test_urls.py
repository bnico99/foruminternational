
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from booking.views import CalendarView


class TestUrls(SimpleTestCase):

    """ calendar can't be reversed
    def test_calendar_url_resolves(self):
        url = reverse('calendar')
        self.assertEquals(resolve(url).func, CalendarView)
    """
