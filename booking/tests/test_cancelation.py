from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase
from django.db import models
from booking.models import Event, Blocker, Booking
import datetime as dt
from booking.models import Booking, get_date_availability, Availability, CancelledBooking
import datetime


class TestModels(TestCase):

    def test_cancel_gone_weekday(self):
        # create normal booking
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
        # check if Availability is LOW
        self.assertEqual(get_date_availability(dt.date(2020, 1, 1)), Availability(2))

        # cancel booking, delete original booking, check availability
        canceledbooking = CancelledBooking.create(event_to_cancel=booking)
        canceledbooking.save()
        booking.delete()
        self.assertEqual(get_date_availability(dt.date(2020, 1, 1)), Availability(1))

        # check, if the canceled booking was saved
        getcancel = CancelledBooking.objects.get(rent=20)
        if (not (getcancel)):
            # can't find canceled booking, something went wrong
            self.assertEqual(0, 1)
        else:
            # check if all fields are true
            self.assertEqual(getcancel.end_datetime, dt.datetime(2020, 1, 1, 19, 0))
            self.assertEqual(getcancel.author, user)
            self.assertEqual(getcancel.rent, 20)
            self.assertEqual(getcancel.rent_was_paid, False)
            self.assertEqual(getcancel.rent_paid_back, False)

    def test_cancel_gone_weekend(self):
        # create normal booking
        user = User.objects.create(id=1, is_staff=True)
        booking = Booking.objects.create(date=dt.date(2020, 1, 4),

                                         start_time=dt.time(16, 0),
                                         duration=12,
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
        # check if Availability is LOW
        self.assertEqual(get_date_availability(dt.date(2020, 1, 4)), Availability(3))

        # cancel booking, delete original booking, check availability
        canceledbooking = CancelledBooking.create(event_to_cancel=booking)
        canceledbooking.save()
        booking.delete()
        self.assertEqual(get_date_availability(dt.date(2020, 1, 4)), Availability(1))

        # check, if the canceled booking was saved
        getcancel = CancelledBooking.objects.get(rent=165)
        if (not (getcancel)):
            # can't find canceled booking, something went wrong
            self.assertEqual(0, 1)
        else:
            # check if all fields are true
            self.assertEqual(getcancel.end_datetime, dt.datetime(2020, 1, 5, 4, 0))
            self.assertEqual(getcancel.author, user)
            self.assertEqual(getcancel.rent, 165)
            self.assertEqual(getcancel.rent_was_paid, False)
            self.assertEqual(getcancel.rent_paid_back, False)

    def test_cancel_two_bookings_correct_canceled(self):
        # create two bookings, so we can check if the correct one is canceled
        user = User.objects.create(id=1, is_staff=True)
        booking1 = Booking.objects.create(date=dt.date(2020, 1, 1),

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
        booking1.save()
        booking2 = Booking.objects.create(date=dt.date(2020, 1, 4),

                                          start_time=dt.time(16, 0),
                                          duration=12,
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
        booking2.save()
        # check if Availability is LOW
        self.assertEqual(get_date_availability(dt.date(2020, 1, 4)), Availability(3))

        # cancel booking2, delete booking2, check availability
        canceledbooking = CancelledBooking.create(event_to_cancel=booking2)
        canceledbooking.save()
        booking2.delete()
        self.assertEqual(get_date_availability(dt.date(2020, 1, 4)), Availability(1))

        # check, if the canceled booking was saved
        getcancel = CancelledBooking.objects.get(rent=165)
        if (not (getcancel)):
            # can't find canceled booking, something went wrong
            self.assertEqual(0, 1)
        else:
            # check if all fields are true
            self.assertEqual(getcancel.end_datetime, dt.datetime(2020, 1, 5, 4, 0))
            self.assertEqual(getcancel.author, user)
            self.assertEqual(getcancel.rent, 165)
            self.assertEqual(getcancel.rent_was_paid, False)
            self.assertEqual(getcancel.rent_paid_back, False)
