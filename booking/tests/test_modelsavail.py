from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase
from django.db import models
from booking.models import Event, Blocker, Booking, get_date_availability, Availability
import datetime as dt


class TestModels(TestCase):




    # Testing the case: # underWeek # Student # under50 # 3h# norefigerator # notoiletsneeded # expected outcome 20
    def test_get_date_availability_allfree(self):

        self.assertEqual(get_date_availability(dt.date(2020, 1, 1)), Availability(1))

    def test_get_date_availability_free(self):
        user = User.objects.create(id=1, is_staff=True)
        booking = Booking.objects.create(date=dt.date(2020, 1, 1),

                                         start_time=dt.time(16, 0),
                                         duration=3,
                                         student='yes',
                                         number_people=5,
                                         refrigerator='no',
                                         occasion='',
                                         confirmed=False,
                                         rent_paid=False,
                                         contract_signed=False,
                                         deposit_paid=False,
                                         deposit_refunded=False,
                                         author=user)
        booking.save()
        self.assertEqual(get_date_availability(dt.date(2020, 1, 2)), Availability(1))

    #if the room is booked for 6 ours under the week: 16+6-> 22 hours: the room cannot be booked any more
    def test_get_date_availability_lowunderweek (self):
        user = User.objects.create(id=1, is_staff=True)
        booking = Booking.objects.create(date=dt.date(2020, 1, 1),

                                         start_time=dt.time(16, 0),
                                         duration=6,
                                         student='yes',
                                         number_people=5,
                                         refrigerator='no',
                                         occasion='',
                                         confirmed=False,
                                         rent_paid=False,
                                         contract_signed=False,
                                         deposit_paid=False,
                                         deposit_refunded=False,
                                         author=user)
        booking.save()
        self.assertEqual(get_date_availability(dt.date(2020, 1, 1)), Availability(2))

    # starting at 9h , there is no other time bookable anymore
    # furthermore the next day should still be completely free
    def test_get_date_availability_fullunderweek2 (self):
        user = User.objects.create(id=1, is_staff=True)
        booking = Booking.objects.create(date=dt.date(2020, 1, 1),

                                         start_time=dt.time(18, 0),
                                         duration=9,
                                         student='yes',
                                         number_people=5,
                                         refrigerator='no',
                                         occasion='',
                                         confirmed=False,
                                         rent_paid=False,
                                         contract_signed=False,
                                         deposit_paid=False,
                                         deposit_refunded=False,
                                         author=user)
        booking.save()
        self.assertEqual(get_date_availability(dt.date(2020, 1, 1)), Availability(3))
        self.assertEqual(get_date_availability(dt.date(2020, 1, 2)), Availability(1))

    # if everthing is full, but only 23.00 not, the day should be low not full

    def test_get_date_availability_almostfull(self):
        user = User.objects.create(id=1, is_staff=True)
        booking = Booking.objects.create(date=dt.date(2020, 1, 1),

                                         start_time=dt.time(17, 0),
                                         duration=6,
                                         student='yes',
                                         number_people=5,
                                         refrigerator='no',
                                         occasion='',
                                         confirmed=False,
                                         rent_paid=False,
                                         contract_signed=False,
                                         deposit_paid=False,
                                         deposit_refunded=False,
                                         author=user)
        booking.save()
        self.assertEqual(get_date_availability(dt.date(2020, 1, 1)), Availability(2))

    #there are some free hours, but still nothing bookable
    def test_get_date_availability_fullunderweek3(self):
        user = User.objects.create(id=100, is_staff=True)
        booking = Booking.objects.create(date=dt.date(2020, 1, 1),

                                         start_time=dt.time(23, 0),
                                         duration=6,
                                         student='yes',
                                         number_people=5,
                                         refrigerator='no',
                                         occasion='',
                                         confirmed=False,
                                         rent_paid=False,
                                         contract_signed=False,
                                         deposit_paid=False,
                                         deposit_refunded=False,
                                         author=user)
        booking1 = Booking.objects.create(date=dt.date(2020, 1, 1),

                                         start_time=dt.time(18, 0),
                                         duration=3,
                                         student='yes',
                                         number_people=5,
                                         refrigerator='no',
                                         occasion='',
                                         confirmed=False,
                                         rent_paid=False,
                                         contract_signed=False,
                                         deposit_paid=False,
                                         deposit_refunded=False,
                                         author=user)
        booking.save()
        booking1.save()
        self.assertEqual(get_date_availability(dt.date(2020, 1, 1)), Availability(3))




