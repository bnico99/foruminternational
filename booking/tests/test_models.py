from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase
from django.db import models
from booking.models import Event, Blocker, Booking
import datetime as dt


class TestModels(TestCase):




    # Testing the case: # underWeek # Student # under50 # 3h# norefigerator # notoiletsneeded # expected outcome 20
    def test_price1(self):
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
        t = booking.calculate_price_event(),
        self.assertEqual(t, (20.0,))

    # Testing the case: #underWeek # Student # under50 # 3h # refigerator# notoiletsneeded # expected outcome 20
    def test_price2(self):
            user = User.objects.create(id=1, is_staff=True)
            booking = Booking.objects.create(date=dt.date(2020, 1, 1),

                                             start_time=dt.time(16, 0),
                                             duration=3,
                                             student='yes',
                                             number_people=5,
                                             refrigerator='yes',
                                             occasion='',
                                             confirmed=False,
                                             rent_paid=False,
                                             contract_signed=False,
                                             deposit_paid=False,
                                             deposit_refunded=False,
                                             author=user)
            t = booking.calculate_price_event(),
            self.assertEqual(t, (20.0,))

   # Testing the case: # underWeek # Student # under50 # 6h # norefigerator # notoiletsneeded # expected outcome 40
    def test_price3(self):
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
               t = booking.calculate_price_event(),
               self.assertEqual(t, (40.0,))

   # Testing the case: # underWeek # Student # under50 # 9h # norefigerator # toilets should always be needed # expected outcome 120
    def test_price4(self):
       user = User.objects.create(id=1, is_staff=True)
       booking = Booking.objects.create(date=dt.date(2020, 1, 1),

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
       t = booking.calculate_price_event(),
       self.assertEqual(t, (120.0,))

       # Testing the case: # underWeek # Student # under50 # 6h # norefigerator # toilets needed because of starting time # expected outcome 80
    def test_price5(self):
          user = User.objects.create(id=1, is_staff=True)
          booking = Booking.objects.create(date=dt.date(2020, 1, 1),

                                           start_time=dt.time(18, 0),
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
          t = booking.calculate_price_event(),
          self.assertEqual(t, (80.0,))
# Testing the case: # underWeek # Student # under50 # 3h # norefigerator # toilets should be needed becuase of statrting time # expected outcome 60
    def test_price6(self):
       user = User.objects.create(id=1, is_staff=True)
       booking = Booking.objects.create(date=dt.date(2020, 1, 1),

                                        start_time=dt.time(22, 0),
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
       t = booking.calculate_price_event(),
       self.assertEqual(t, (60.0,))
# Testing the case: # underWeek # Student # over50 # 3h # norefigerator # toilets not needed # expected outcome 40
    def test_price7(self):
       user = User.objects.create(id=1, is_staff=True)
       booking = Booking.objects.create(date=dt.date(2020, 1, 1),

                                        start_time=dt.time(16, 0),
                                        duration=3,
                                        student='yes',
                                        number_people=55,
                                        refrigerator='no',
                                        occasion='',
                                        confirmed=False,
                                        rent_paid=False,
                                        contract_signed=False,
                                        deposit_paid=False,
                                        deposit_refunded=False,
                                        author=user)
       t = booking.calculate_price_event(),
       self.assertEqual(t, (40.0,))
# Testing the case: # underWeek # Student # over50 # 3h # norefigerator # toilets should be needed becasuse of starting time # expected outcome 80
    def test_price8(self):
       user = User.objects.create(id=1, is_staff=True)
       booking = Booking.objects.create(date=dt.date(2020, 1, 1),

                                        start_time=dt.time(22, 0),
                                        duration=3,
                                        student='yes',
                                        number_people=55,
                                        refrigerator='no',
                                        occasion='',
                                        confirmed=False,
                                        rent_paid=False,
                                        contract_signed=False,
                                        deposit_paid=False,
                                        deposit_refunded=False,
                                        author=user)
       t = booking.calculate_price_event(),
       self.assertEqual(t, (80.0,))

# Testing the case: # underWeek # Student # over50 # 6h # norefigerator #no toilets # expected outcome 70
    def test_price9(self):
       user = User.objects.create(id=1, is_staff=True)
       booking = Booking.objects.create(date=dt.date(2020, 1, 1),

                                        start_time=dt.time(16, 0),
                                        duration=6,
                                        student='yes',
                                        number_people=55,
                                        refrigerator='no',
                                        occasion='',
                                        confirmed=False,
                                        rent_paid=False,
                                        contract_signed=False,
                                        deposit_paid=False,
                                        deposit_refunded=False,
                                        author=user)
       t = booking.calculate_price_event(),
       self.assertEqual(t, (70.0,))
  # Testing the case: # underWeek # Student # over50 # 6h # norefigerator # toilets should be needed becasuse of starting time # expected outcome 110

    def test_price10(self):
       user = User.objects.create(id=1, is_staff=True)
       booking = Booking.objects.create(date=dt.date(2020, 1, 1),

                                        start_time=dt.time(17, 0),
                                        duration=6,
                                        student='yes',
                                        number_people=55,
                                        refrigerator='no',
                                        occasion='',
                                        confirmed=False,
                                        rent_paid=False,
                                        contract_signed=False,
                                        deposit_paid=False,
                                        deposit_refunded=False,
                                        author=user)
       t = booking.calculate_price_event(),
       self.assertEqual(t, (110.0,))

    # Testing the case: # underWeek # Student # over50 # 9h # norefigerator # toilets should be needed because always needed # expected outcome 170
    def test_price11(self):
       user = User.objects.create(id=1, is_staff=True)
       booking = Booking.objects.create(date=dt.date(2020, 1, 1),

                                    start_time=dt.time(17, 0),
                                    duration=12,
                                    student='yes',
                                    number_people=55,
                                    refrigerator='no',
                                    occasion='',
                                    confirmed=False,
                                    rent_paid=False,
                                    contract_signed=False,
                                    deposit_paid=False,
                                    deposit_refunded=False,
                                    author=user)
       t = booking.calculate_price_event(),
       self.assertEqual(t, (170.0,))

       # Testing the case: # underWeek # noStudent # under50 # 6h # norefigerator # notoiletsneeded # expected outcome 40
    def test_price12(self):
           user = User.objects.create(id=1, is_staff=True)
           booking = Booking.objects.create(date=dt.date(2020, 1, 1),

                                            start_time=dt.time(16, 0),
                                            duration=3,
                                            student='no',
                                            number_people=5,
                                            refrigerator='yes',
                                            occasion='',
                                            confirmed=False,
                                            rent_paid=False,
                                            contract_signed=False,
                                            deposit_paid=False,
                                            deposit_refunded=False,
                                            author=user)
           t = booking.calculate_price_event(),
           self.assertEqual(t, (40.0,))

   # Testing the case: # underWeek # noStudent # under50 # 6h # norefigerator # notoiletsneeded # expected outcome 70
    def test_price13(self):
           user = User.objects.create(id=1, is_staff=True)
           booking = Booking.objects.create(date=dt.date(2020, 1, 1),

                                            start_time=dt.time(16, 0),
                                            duration=6,
                                            student='no',
                                            number_people=5,
                                            refrigerator='no',
                                            occasion='',
                                            confirmed=False,
                                            rent_paid=False,
                                            contract_signed=False,
                                            deposit_paid=False,
                                            deposit_refunded=False,
                                            author=user)
           t = booking.calculate_price_event(),
           self.assertEqual(t, (70.0,))

       # Testing the case: # underWeek # noStudent # under50 # 9h # norefigerator # toilets should always be needed # expected outcome 165
    def test_price14(self):
           user = User.objects.create(id=1, is_staff=True)
           booking = Booking.objects.create(date=dt.date(2020, 1, 1),

                                            start_time=dt.time(16, 0),
                                            duration=12,
                                            student='no',
                                            number_people=5,
                                            refrigerator='no',
                                            occasion='',
                                            confirmed=False,
                                            rent_paid=False,
                                            contract_signed=False,
                                            deposit_paid=False,
                                            deposit_refunded=False,
                                            author=user)
           t = booking.calculate_price_event(),
           self.assertEqual(t, (165.0,))

     # Testing the case: # underWeek # noStudent # under50 # 6h # norefigerator # toilets needed because of starting time # expected outcome 110
    def test_price15(self):
           user = User.objects.create(id=1, is_staff=True)
           booking = Booking.objects.create(date=dt.date(2020, 1, 1),

                                            start_time=dt.time(18, 0),
                                            duration=6,
                                            student='no',
                                            number_people=5,
                                            refrigerator='no',
                                            occasion='',
                                            confirmed=False,
                                            rent_paid=False,
                                            contract_signed=False,
                                            deposit_paid=False,
                                            deposit_refunded=False,
                                            author=user)
           t = booking.calculate_price_event(),
           self.assertEqual(t, (110.0,))

      # Testing the case: # underWeek # Student # under50 # 3h # norefigerator # toilets should be needed becuase of statrting time # expected outcome 80
    def test_price16(self):
           user = User.objects.create(id=1, is_staff=True)
           booking = Booking.objects.create(date=dt.date(2020, 1, 1),

                                            start_time=dt.time(22, 0),
                                            duration=3,
                                            student='no',
                                            number_people=5,
                                            refrigerator='no',
                                            occasion='',
                                            confirmed=False,
                                            rent_paid=False,
                                            contract_signed=False,
                                            deposit_paid=False,
                                            deposit_refunded=False,
                                            author=user)
           t = booking.calculate_price_event(),
           self.assertEqual(t, (80.0,))

       # Testing the case: # underWeek # Student # over50 # 3h # norefigerator # toilets not needed # expected outcome 65
    def test_price17(self):
           user = User.objects.create(id=1, is_staff=True)
           booking = Booking.objects.create(date=dt.date(2020, 1, 1),

                                            start_time=dt.time(16, 0),
                                            duration=3,
                                            student='no',
                                            number_people=55,
                                            refrigerator='no',
                                            occasion='',
                                            confirmed=False,
                                            rent_paid=False,
                                            contract_signed=False,
                                            deposit_paid=False,
                                            deposit_refunded=False,
                                            author=user)
           t = booking.calculate_price_event(),
           self.assertEqual(t, (65.0,))

       # Testing the case: # underWeek # Student # over50 # 3h # norefigerator # toilets should be needed becasuse of starting time # expected outcome 105
    def test_price18(self):
           user = User.objects.create(id=1, is_staff=True)
           booking = Booking.objects.create(date=dt.date(2020, 1, 1),

                                            start_time=dt.time(22, 0),
                                            duration=3,
                                            student='no',
                                            number_people=55,
                                            refrigerator='no',
                                            occasion='',
                                            confirmed=False,
                                            rent_paid=False,
                                            contract_signed=False,
                                            deposit_paid=False,
                                            deposit_refunded=False,
                                            author=user)
           t = booking.calculate_price_event(),
           self.assertEqual(t, (105.0,))

       # Testing the case: # underWeek # Student # over50 # 6h # norefigerator #no toilets # expected outcome 110
    def test_price19(self):
           user = User.objects.create(id=1, is_staff=True)
           booking = Booking.objects.create(date=dt.date(2020, 1, 1),

                                            start_time=dt.time(16, 0),
                                            duration=6,
                                            student='no',
                                            number_people=55,
                                            refrigerator='no',
                                            occasion='',
                                            confirmed=False,
                                            rent_paid=False,
                                            contract_signed=False,
                                            deposit_paid=False,
                                            deposit_refunded=False,
                                            author=user)
           t = booking.calculate_price_event(),
           self.assertEqual(t, (110.0,))

       # Testing the case: # underWeek # Student # over50 # 6h # norefigerator # toilets should be needed becasuse of starting time # expected outcome 150

    def test_price20(self):
           user = User.objects.create(id=1, is_staff=True)
           booking = Booking.objects.create(date=dt.date(2020, 1, 1),

                                            start_time=dt.time(17, 0),
                                            duration=6,
                                            student='no',
                                            number_people=55,
                                            refrigerator='no',
                                            occasion='',
                                            confirmed=False,
                                            rent_paid=False,
                                            contract_signed=False,
                                            deposit_paid=False,
                                            deposit_refunded=False,
                                            author=user)
           t = booking.calculate_price_event(),
           self.assertEqual(t, (150.0,))

       # Testing the case: # underWeek # Student # over50 # 9h # norefigerator # toilets should be needed because always needed # expected outcome 190
    def test_price21(self):
           user = User.objects.create(id=1, is_staff=True)
           booking = Booking.objects.create(date=dt.date(2020, 1, 1),

                                            start_time=dt.time(17, 0),
                                            duration=12,
                                            student='no',
                                            number_people=55,
                                            refrigerator='no',
                                            occasion='',
                                            confirmed=False,
                                            rent_paid=False,
                                            contract_signed=False,
                                            deposit_paid=False,
                                            deposit_refunded=False,
                                            author=user)
           t = booking.calculate_price_event(),
           self.assertEqual(t, (190.0,))

    # Testing the case: #Weekend #Student #12h # expected outcome 165
    def test_price22(self):
        user = User.objects.create(id=1, is_staff=True)
        booking = Booking.objects.create(date=dt.date(2020, 1, 12),

                                         start_time=dt.time(10, 0),
                                         duration=12,
                                         student='yes',
                                         number_people= 5,
                                         refrigerator='no',
                                         occasion='',
                                         confirmed=False,
                                         rent_paid=False,
                                         contract_signed=False,
                                         deposit_paid=False,
                                         deposit_refunded=False,
                                         author=user)
        t = booking.calculate_price_event(),
        self.assertEqual(t, (165.0,))

    # Testing the case: #Weekend #Student #24h # expected outcome 280
    def test_price23(self):
        user = User.objects.create(id=1, is_staff=True)
        booking = Booking.objects.create(date=dt.date(2020, 1, 12),

                                         start_time=dt.time(10, 0),
                                         duration=24,
                                         student='yes',
                                         number_people=125,
                                         refrigerator='no',
                                         occasion='',
                                         confirmed=False,
                                         rent_paid=False,
                                         contract_signed=False,
                                         deposit_paid=False,
                                         deposit_refunded=False,
                                         author=user)
        t = booking.calculate_price_event(),
        self.assertEqual(t, (280.0,))

        # Testing the case: #Weekend #noStudent  12h # expected outcome 265
    def test_price24(self):
            user = User.objects.create(id=1, is_staff=True)
            booking = Booking.objects.create(date=dt.date(2020, 1, 12),

                                             start_time=dt.time(10, 0),
                                             duration=12,
                                             student='no',
                                             number_people=5,
                                             refrigerator='no',
                                             occasion='',
                                             confirmed=False,
                                             rent_paid=False,
                                             contract_signed=False,
                                             deposit_paid=False,
                                             deposit_refunded=False,
                                             author=user)
            t = booking.calculate_price_event(),
            self.assertEqual(t, (265.0,))

    # Testing the case: #Weekend #noStudent 24h # expected outcome 380
    def test_price25(self):
        user = User.objects.create(id=1, is_staff=True)
        booking = Booking.objects.create(date=dt.date(2020, 1, 12),

                                         start_time=dt.time(10, 0),
                                         duration=24,
                                         student='no',
                                         number_people=50,
                                         refrigerator='no',
                                         occasion='',
                                         confirmed=False,
                                         rent_paid=False,
                                         contract_signed=False,
                                         deposit_paid=False,
                                         deposit_refunded=False,
                                         author=user)
        t = booking.calculate_price_event(),
        self.assertEqual(t, (380.0,))


