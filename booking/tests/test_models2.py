from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase
from django.db import models
from booking.models import Event, Blocker, Booking
import datetime


class TestModels(TestCase):




  def setUp(self):
    d = datetime.date(2020, 1, 1)
    event1 = Event.objects.create(
        date=d,
        start_time=datetime.time(10, 0),
        duration=6
    )

  def test_event(self):
    d = datetime.date(2020, 1, 1)
    event1 = Event.objects.create(
        date=d,
        start_time=datetime.time(10, 0),
        duration=6)
    f = event1.is_blocker()
    self.assertFalse(f)


  def test_eventsave(self):
    d = datetime.date(2020, 1, 1)
    event1 = Event.objects.create(
        date=d,
        start_time=datetime.time(10, 0),
        duration=6)
    event1.save()

    self.assertEqual(event1.start_datetime, datetime.datetime(2020, 1, 1, 10 , 0))
    self.assertEqual(event1.end_datetime, datetime.datetime(2020, 1, 1, 16 , 0))

  def test_eventsaveover0(self):
    d = datetime.date(2020, 1, 1)
    event1 = Event.objects.create(
        date=d,
        start_time=datetime.time(22, 0),
        duration=3)
    event1.save()

    self.assertEqual(event1.start_datetime, datetime.datetime(2020, 1, 1, 22 , 0))
    self.assertEqual(event1.end_datetime, datetime.datetime(2020, 1, 2, 1 , 0))

