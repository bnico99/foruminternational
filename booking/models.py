from abc import abstractmethod
from datetime import timedelta
from enum import Enum

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.datetime_safe import datetime
from django.utils import timezone
from docxtpl import DocxTemplate
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.utils.translation import get_language
import datetime as dt
from user_account.models import Profile
from django import forms
import django.utils.timezone as tz

from info.models import PriceEntry, MailEntry
from website import settings
from django.core.exceptions import ValidationError


class Event(models.Model):
    """Abstract representation of an event"""
    date = models.DateField(_('Datum'), help_text=_('Bitte wählen Sie ein Datum aus.'))
    start_time = models.TimeField(_('Beginn'), help_text=_('Bitte wählen Sie eine Uhrzeit aus.'))

    duration = models.SmallIntegerField(_('Dauer'), help_text=_('Bitte wählen Sie die gewünschte Dauer.'))

    # Internal fields
    start_datetime = models.DateTimeField(default='', editable=False)
    end_datetime = models.DateTimeField(default='', editable=False)
    booking_time = models.DateTimeField(default=timezone.now, editable=False)

    # Fill internal fields
    def save(self, *args, **kwargs):
        self.start_datetime = datetime.combine(self.date, self.start_time)
        self.end_datetime = self.start_datetime + dt.timedelta(hours=self.duration)
        super().save(*args, **kwargs)

    def update(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @abstractmethod
    def is_blocker(self):
        pass


class WaitingList(models.Model):
    """Abstract representation of a waiting list for a certain date"""
    date = models.DateField("Datum", default="2019-01-01")  # the date of the waiting list
    waiting = models.ManyToManyField(Profile)  # users waiting for this date to get free

    def remind_customers(self):
        for customer in self.waiting.all():
            # construct and send email message to the customer
            context = {
                'date': self.date,
                'customer': customer,
            }

            mail_text = render_to_string('mails/customer_waiting_list.txt', context=context)

            send_mail(
                'Warteliste FORUM International ' + self.date.strftime("%d.%m.%Y"),
                mail_text,
                settings.EMAIL_HOST_USER,
                [customer.email],
                fail_silently=False,
            )


class Blocker(Event):
    """Class used to block timeslots without a booking"""

    def is_blocker(self):
        return True

    def __str__(self):
        return 'Blocker vom {}, {}, {}'.format(self.date, self.start_time, self.duration)


class Booking(Event):
    """Representation of a booking"""
    YES_NO = [
        ("yes", _("JA")),
        ("no", _("NEIN")),
    ]

    student = models.CharField(_('Student (UdS/HTW)'), choices=YES_NO, max_length=10,
                               default='',
                               help_text=_('Bitte geben Sie an, ob Sie Student der UdS oder der HTW sind.'))

    number_people = models.SmallIntegerField(_('Personenzahl'),
                                             help_text=_(
                                                 'Bitte geben Sie an, wie viele Personen etwa erscheinen werden.   '))

    refrigerator = models.CharField(_('Kühlschränke erwünscht?'), choices=YES_NO, max_length=10,
                                    default='',
                                    help_text=_(
                                        'Bitte geben Sie an, ob Sie die Kühlschränke des FORUM international benutzen möchten.'))

    occasion = models.TextField(_('Anlass'), max_length=40,
                                default='', help_text=_('Bitte geben Sie einen Anlass an.'))

    confirmed = models.BooleanField(_('Bestätigt'), default=False, help_text='')
    rent_paid = models.BooleanField(_('Miete bezahlt'), default=False, help_text='')
    contract_signed = models.BooleanField(_('Vertrag unterschrieben'), default=False, help_text='')
    deposit_paid = models.BooleanField(_('Kaution gezahlt'), default=False, help_text='')
    deposit_refunded = models.BooleanField(_('Kaution zurückerstattet'), default=False, help_text='')

    requested_inspection = models.BooleanField(_('Besichtigung beantragt'), default=False, help_text='')

    author = models.ForeignKey(User, default=None, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        # self.start_datetime = datetime.combine(self.date, self.start_time)
        # self.end_datetime = self.start_datetime + dt.timedelta(hours=self.duration)
        super().save(*args, **kwargs)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)

    def __str__(self):
        return 'Buchung vom {}, {}, {}'.format(self.date, self.start_time, self.duration)

    def calculate_price_event(self):
        """Calculate and return the price for the event."""
        return calculate_price(self.date, str_to_bool(self.student), self.duration, self.number_people,
                               self.end_datetime,
                               str_to_bool(self.refrigerator))

    def generate_contract(self):
        """Generate the contract for the event and save it in /data/generated_contracts/date_authorid.docx."""
        template = open("data/contract_template.docx", "rb")
        contract = DocxTemplate(template)

        if (self.date - self.booking_time.date()) < dt.timedelta(days=14):
            return_date = (self.booking_time + dt.timedelta(days=1)).strftime("%d.%m.%Y")
        else:
            return_date = (self.booking_time + dt.timedelta(days=7)).strftime("%d.%m.%Y")

        if self.refrigerator == 'yes':
            included = 'Toilettennutzung und Kühlhaus'
        else:
            included = 'Toilettennutzung'

        context = {
            'customer': self.author.profile,
            'start_datetime': self.start_datetime.strftime("%d.%m.%Y, %H:%M"),
            'end_datetime': self.end_datetime.strftime("%d.%m.%Y, %H:%M"),
            'duration': self.duration,
            'price': self.calculate_price_event(),
            'deposit': PriceEntry.objects.get(title='Deposit').text,
            'current_date': self.booking_time.strftime("%d.%m.%Y"),
            'return_date': return_date,
            'tutor_mail': MailEntry.objects.get(title='Tutor').mail,
            'included': included,
        }

        contract.render(context)
        contract.save(
            'data/generated_contracts/contract_' + self.start_datetime.__str__() + '_' + str(self.author_id) + '.docx')

    def generate_bill(self):
        """Generate the contract for the event and save it in /data/generated_bills/date_authorid.docx."""
        # Check if day is a weekday
        day_type = get_day_type(self.start_datetime)

        if day_type == 'WEEKEND' or (self.end_datetime.time() > dt.time(22, 0, 0)
                                     or self.end_datetime.time() < dt.time(8, 0, 0)):
            toilet = "inkl. Nutzung der Toiletten im FORUM International"

        else:
            toilet = "Toilettennutzung der Mensa im Erdgeschoss, D4.1"

        template = open("data/bill_template.docx", "rb")
        bill = DocxTemplate(template)
        context = {
            'customer': self.author.profile,
            'bill_id': self.id,
            'current_year': self.booking_time.strftime("%Y"),
            'customer_title': self.author.profile.title,
            'customer_lastname': self.author.profile.last_name,
            'start_datetime': self.start_datetime.strftime("%d.%m.%Y, %H:%M"),
            'end_datetime': self.end_datetime.strftime("%d.%m.%Y, %H:%M"),
            'duration': self.duration,
            'price': self.calculate_price_event(),
            'current_date': self.booking_time.strftime("%d.%m.%Y"),
            'toilet': toilet
        }

        bill.render(context)
        bill.save(
            'data/generated_bills/bill_' + self.start_datetime.__str__() + '_' + str(self.author_id) + '.docx')

    def is_blocker(self):
        """Return if the booking is a blocker."""
        return False

    def send_email_caretaker(self):
        """If refrigeration is needed, send mail to the caretaker mail address saved in database including all info."""
        # check if refrigerator is needed and if yes send email to caretaker
        if self.refrigerator:
            # get date and time of event
            date = self.date.strftime("%d.%m.%Y")
            time = self.start_time.strftime("%H:%M")

            # construct and send email message to caretaker
            context = {
                'date': date,
                'time': time,
            }
            mail_text = render_to_string('mails/caretaker.txt', context=context)
            send_mail(
                'Buchung FORUM international ' + date,
                mail_text,
                settings.EMAIL_HOST_USER,
                [MailEntry.objects.get(title='Caretaker').mail],
                fail_silently=False,
            )
        return

    def send_cancellation_email_caretaker(self):
        """
        If refrigeration was needed, send cancellation mail to the caretaker mail address
        saved in database including all info.
        """
        # check if refrigerator was needed and if yes send email to caretaker
        if self.refrigerator:
            # get date and time of event
            date = self.date.strftime("%d.%m.%Y")
            time = self.start_time.strftime("%H:%M")

            # construct and send email message to caretaker
            context = {
                'date': date,
                'time': time,
            }
            mail_text = render_to_string('mails/caretaker_cancelled.txt', context=context)
            send_mail(
                'Stornierte Buchung FORUM international ' + date,
                mail_text,
                settings.EMAIL_HOST_USER,
                [MailEntry.objects.get(title='Caretaker').mail],
                fail_silently=False,
            )
        return

    def send_email_cleaning(self):
        """Send mail to the cleaning mail address saved in database including all info."""
        start_datetime = self.start_datetime.strftime("%d.%m.%Y, %H:%M")
        end_datetime = self.end_datetime.strftime("%d.%m.%Y, %H:%M")

        # construct and send email message to caretaker
        context = {
            'start_datetime': start_datetime,
            'end_datetime': end_datetime,
        }
        mail_text = render_to_string('mails/cleaning.txt', context=context)
        send_mail(
            'Buchung FORUM international ' + start_datetime,
            mail_text,
            settings.EMAIL_HOST_USER,
            [MailEntry.objects.get(title='Cleaning').mail],
            fail_silently=False,
        )
        return

    def send_cancellation_email_cleaning(self):
        """Send cancellation mail to the cleaning mail address saved in database including all info."""
        start_datetime = self.start_datetime.strftime("%d.%m.%Y, %H:%M")
        end_datetime = self.end_datetime.strftime("%d.%m.%Y, %H:%M")

        # construct and send email message to caretaker
        context = {
            'start_datetime': start_datetime,
            'end_datetime': end_datetime,
        }
        mail_text = render_to_string('mails/cleaning_cancelled.txt', context=context)
        send_mail(
            'Stornierte Buchung FORUM international ' + start_datetime,
            mail_text,
            settings.EMAIL_HOST_USER,
            [MailEntry.objects.get(title='Cleaning').mail],
            fail_silently=False,
        )
        return

    def send_email_tutor(self):
        """Send mail to the tutor mail address saved in database including all info."""
        # get date, time and customer of event
        start_datetime = self.start_datetime.strftime("%d.%m.%Y, %H:%M")
        end_datetime = self.end_datetime.strftime("%d.%m.%Y, %H:%M")
        customer = self.author.profile

        # construct and send email message to tutor
        context = {
            'start_datetime': start_datetime,
            'end_datetime': end_datetime,
            'customer': customer,
        }
        mail_text = render_to_string('mails/tutor.txt', context=context)
        send_mail(
            'Buchung FORUM international ' + start_datetime,
            mail_text,
            settings.EMAIL_HOST_USER,
            [MailEntry.objects.get(title='Tutor').mail],
            fail_silently=False,
        )
        return

    def send_cancellation_email_tutor(self):
        """Send cancellation mail to the cleaning mail address saved in database including all info."""
        # get date and time of event
        start_datetime = self.start_datetime.strftime("%d.%m.%Y, %H:%M")
        end_datetime = self.end_datetime.strftime("%d.%m.%Y, %H:%M")

        # construct and send email message to tutor
        context = {
            'start_datetime': start_datetime,
            'end_datetime': end_datetime,
        }
        mail_text = render_to_string('mails/tutor_cancelled.txt', context=context)
        send_mail(
            'Stornierte Buchung FORUM international ' + start_datetime,
            mail_text,
            settings.EMAIL_HOST_USER,
            [MailEntry.objects.get(title='Tutor').mail],
            fail_silently=False,
        )
        return

    def send_email_admin(self):
        """Send mail to the admin mail address saved in database including all info."""
        # get date, time, customer, student status and occasion of event
        start_datetime = self.start_datetime.strftime("%d.%m.%Y, %H:%M")
        end_datetime = self.end_datetime.strftime("%d.%m.%Y, %H:%M")
        customer = self.author.profile
        occasion = self.occasion
        student = self.student.__str__()

        # construct and send email message to admin
        context = {
            'start_datetime': start_datetime,
            'end_datetime': end_datetime,
            'customer': customer,
            'student': student,
            'occasion': occasion,
        }
        mail_text = render_to_string('mails/admin.txt', context=context)
        send_mail(
            'Buchung FORUM international ' + start_datetime,
            mail_text,
            settings.EMAIL_HOST_USER,
            [MailEntry.objects.get(title='Admin').mail],
            fail_silently=False,
        )
        return

    def send_cancellation_email_admin(self):
        """Send cancellation mail to the cleaning mail address saved in database including all info."""
        # get date, time, customer and occasion of event
        start_datetime = self.start_datetime.strftime("%d.%m.%Y, %H:%M")
        end_datetime = self.end_datetime.strftime("%d.%m.%Y, %H:%M")
        customer = self.author.profile
        occasion = self.occasion

        # construct and send email message to admin
        context = {
            'start_datetime': start_datetime,
            'end_datetime': end_datetime,
            'customer': customer,
            'student': self.student.__str__(),
            'occasion': occasion,
        }
        mail_text = render_to_string('mails/admin_cancelled.txt', context=context)
        send_mail(
            'Stornierte Buchung FORUM international ' + start_datetime,
            mail_text,
            settings.EMAIL_HOST_USER,
            [MailEntry.objects.get(title='Admin').mail],
            fail_silently=False,
        )
        return

    def send_confirmation_email_customer(self, confirmed):
        """
        Send confirmation mail to the customer's mail address including a summary of the booking and the contract
        iff the booking has been confirmed.
        :param confirmed: Boolean indicating whether the booking has been confirmed by the admin
        """
        # get date, time, customer and occasion of event
        start_datetime = self.start_datetime.strftime("%d.%m.%Y, %H:%M")
        end_datetime = self.end_datetime.strftime("%d.%m.%Y, %H:%M")
        customer = self.author.profile
        occasion = self.occasion

        # calculate return date
        if (self.date - self.booking_time.date()) < dt.timedelta(days=14):
            return_date = (self.booking_time + dt.timedelta(days=1)).strftime("%d.%m.%Y")
        else:
            return_date = (self.booking_time + dt.timedelta(days=7)).strftime("%d.%m.%Y")

        # construct and send email message to customer
        context = {
            'start_datetime': start_datetime,
            'end_datetime': end_datetime,
            'customer': customer,
            'student': self.student.__str__(),
            'occasion': occasion,
            'return_date': return_date,
        }

        # construct and send email message to customer
        if confirmed:

            if get_language() == "en":
                mail_text = render_to_string('mails/customer_confirmed_EN.txt', context=context)
                email = EmailMessage(
                    subject='Booking confirmation FORUM international ' + start_datetime,
                    body=mail_text,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[self.author.profile.email],
                )


            else:
                mail_text = render_to_string('mails/customer_confirmed.txt', context=context)
                email = EmailMessage(
                    subject='Buchungsbestätigung FORUM international ' + start_datetime,
                    body=mail_text,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[self.author.profile.email],
                )

            contract = 'data/generated_contracts/contract_' + self.start_datetime.__str__() + '_' + str(
                self.author_id) + '.docx'
            bill = 'data/generated_bills/bill_' + self.start_datetime.__str__() + '_' + str(self.author_id) + '.docx'
            email.attach_file(contract)
            email.attach_file(bill)
            email.send(fail_silently=False)
        else:
            if get_language() == "en":
                mail_text = render_to_string('mails/customer_request_EN.txt', context=context)
                email = EmailMessage(
                    subject='Booking request FORUM international ' + start_datetime,
                    body=mail_text,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[self.author.profile.email],
                )
            else:
                mail_text = render_to_string('mails/customer_request.txt', context=context)
                email = EmailMessage(
                    subject='Anfrage FORUM international ' + start_datetime,
                    body=mail_text,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[self.author.profile.email],
                )

            email.send(fail_silently=False)

        return

    def send_email_customer_paid_contract_received(self):
        """
        Send mail to the customer's mail address when his/her booking has been
        marked as "rent paid" and "contract signed" by the admin
        """
        # get date, time, customer and occasion of event
        start_datetime = self.start_datetime.strftime("%d.%m.%Y, %H:%M")
        end_datetime = self.end_datetime.strftime("%d.%m.%Y, %H:%M")
        customer = self.author.profile
        occasion = self.occasion

        # construct and send email message to customer
        context = {
            'start_datetime': start_datetime,
            'customer': customer,
            'end_datetime': end_datetime,
            'occasion': occasion,
        }

        mail_text = render_to_string('mails/customer_paid_contract_received.txt', context=context)
        email = EmailMessage(
            subject='FORUM International Buchung ' + start_datetime,
            body=mail_text,
            from_email=settings.EMAIL_HOST_USER,
            to=[self.author.profile.email],
        )

        email.send(fail_silently=False)
        return

    def send_reminder_email_customer(self):
        """
        Send mail to the customer's mail address if there are two days left to the
        booking date and the rent has not been paid yet
        """
        # get date, time, customer and occasion of event
        if self.author.is_superuser or self.author.is_staff:
            return

        start_time = self.start_datetime.strftime("%H:%M")
        start_date = self.start_datetime.strftime("%d.%m.%Y.")
        end_datetime = self.end_datetime.strftime("%d.%m.%Y, %H:%M")
        customer = self.author.profile

        # construct and send email message to customer
        context = {
            'start_date': start_date,
            'start_time': start_time,
            'customer': customer,
            'end_datetime': end_datetime,

        }

        mail_text = render_to_string('mails/customer_reminder.txt', context=context)
        email = EmailMessage(
            subject='Zahlungserrinerung FORUM International ' + start_date,
            body=mail_text,
            from_email=settings.EMAIL_HOST_USER,
            to=[self.author.profile.email],
        )

        email.send(fail_silently=False)
        return

    def send_cancellation_email_customer(self, free):
        """
        Send cancellation mail to the customer's mail address
        :param free: Boolean indicating whether the cancellation is free or not
        """
        # get date, time, customer and occasion of event
        start_datetime = self.start_datetime.strftime("%d.%m.%Y, %H:%M")
        end_datetime = self.end_datetime.strftime("%d.%m.%Y, %H:%M")
        customer = self.author.profile
        occasion = self.occasion

        # get date, start time, end time and occasion of event
        context = {
            'start_datetime': start_datetime,
            'end_datetime': end_datetime,
            'customer': customer,
            'occasion': occasion,
        }

        if free:
            # free cancellation
            if get_language() == "en":
                mail_text = render_to_string('mails/customer_cancelled_free_EN.txt', context=context)
                email = EmailMessage(subject='Confirmation for room cancellation FORUM international ' + start_datetime,
                                     body=mail_text,
                                     from_email=settings.EMAIL_HOST_USER,
                                     to=[self.author.profile.email],
                                     )


            else:
                mail_text = render_to_string('mails/customer_cancelled_free.txt', context=context)
                email = EmailMessage(subject='Stornierungsbestätigung FORUM international ' + start_datetime,
                                     body=mail_text,
                                     from_email=settings.EMAIL_HOST_USER,
                                     to=[self.author.profile.email],
                                     )

        else:
            # not a free cancellation
            if get_language() == "en":
                mail_text = render_to_string('mails/customer_cancelled_paid_EN.txt', context=context)
                email = EmailMessage(subject='Confirmation for room cancellation FORUM international ' + start_datetime,
                                     body=mail_text,
                                     from_email=settings.EMAIL_HOST_USER,
                                     to=[self.author.profile.email],
                                     )
            else:
                mail_text = render_to_string('mails/customer_cancelled_paid.txt', context=context)
                email = EmailMessage(subject='Stornierungsbestätigung FORUM international ' + start_datetime,
                                     body=mail_text,
                                     from_email=settings.EMAIL_HOST_USER,
                                     to=[self.author.profile.email],
                                     )

        email.send(fail_silently=False)
        return


class Availability(Enum):
    FREE = 1
    LOW = 2
    FULL = 3


# Automatically called before saving a (new) Booking
@receiver(pre_save, sender=Booking)
def send_booking_mails(sender, instance, **kwargs):
    """Send all necessary mails when a booking is created or updated."""
    new_booking = instance
    try:
        old_booking = sender.objects.get(pk=new_booking.pk)
    except sender.DoesNotExist:
        # Booking has been created
        # Booking could already be confirmed on creation if created by an admin
        if new_booking.confirmed:
            new_booking.generate_contract()
            new_booking.generate_bill()
            new_booking.send_confirmation_email_customer(confirmed=True)
        else:
            new_booking.send_confirmation_email_customer(confirmed=False)

        if new_booking.rent_paid and new_booking.contract_signed:
            new_booking.send_email_customer_paid_contract_received()

        if not (new_booking.author.is_staff or new_booking.author.is_superuser):
            new_booking.send_email_admin()
    else:
        # Booking has only been updated
        if (not old_booking.confirmed) and new_booking.confirmed:
            # Booking has been confirmed by admin
            new_booking.send_email_caretaker()
            new_booking.send_email_cleaning()
            new_booking.generate_contract()
            new_booking.generate_bill()
            new_booking.send_confirmation_email_customer(confirmed=True)
            if not (new_booking.author.is_staff or new_booking.author.is_superuser):
                new_booking.send_email_tutor()

        if (not (
                old_booking.rent_paid and old_booking.contract_signed)) and new_booking.rent_paid and new_booking.contract_signed:
            # Booking has been marked as signed and paid
            new_booking.send_email_customer_paid_contract_received()


def get_date_availability(date):
    """
    Determine whether there are any free slots on a given date and returns a corresponding Availability enum
    :param date: The date to check
    :return: The correct Availability enum
    """
    lasteventhour = 0
    mystart = 16
    datetype = get_day_type(date)
    weekday = date.weekday()
    intotoday = False
    nexthasevents = False

    prevday = date - dt.timedelta(days=1)
    prevevents = Event.objects.filter(date=prevday).values_list('start_datetime', 'end_datetime')
    prelist = []
    for x in prevevents:
        prelist.append(x)
    prelist.sort(key=lambda tup: tup[0])  # sort by starting time
    # all events from the prev day should now be in the prelist
    if prelist:
        if prelist[-1][1].day != prevday.day:
            intotoday = True
            lasteventhour = prelist[-1][1].hour

    events = Event.objects.filter(date=date).values_list('start_datetime', 'end_datetime')
    mylist = []
    # on weekdays only add events after 15 oclock, else it could be blocker
    if datetype == 'WEEKDAY':
        for x in events:
            if x[0].hour > 15:
                mylist.append(x)
    else:
        for x in events:
            mylist.append(x)
    mylist.sort(key=lambda tup: tup[0])  # sort by starting time

    nextday = date + dt.timedelta(days=1)
    nextevents = Event.objects.filter(date=nextday).values_list('start_datetime', 'end_datetime')
    nextlist = []
    for x in nextevents:
        nextlist.append(x)
        nexthasevents = True
    nextlist.sort(key=lambda tup: tup[0])

    if datetype == 'WEEKDAY':
        if mylist:
            mystart = 16
            for event in mylist:
                timedif = event[0].hour - mystart
                if timedif >= 3:
                    # found free 3 hours to book
                    return Availability.LOW
                if event[1].day != date.day:
                    return Availability.FULL
                mystart = event[1].hour
            return Availability.LOW
        else:
            return Availability.FREE
    else:
        # Weekend
        if (weekday != 6):
            # saturday
            if (nexthasevents):
                if (intotoday):
                    # from prev and next has event
                    # start the counting at the first free time
                    # 8 or the end of the event from the prev day, whatever is later
                    mystart = max(lasteventhour, 8)
                    if (mylist):
                        for x in mylist:
                            timedif = x[0].hour - mystart
                            if (timedif >= 12):
                                # found a free timespot
                                return Availability.LOW
                            mystart = x[1].hour
                            if (x[1].day != date.day):
                                # goes into next day and nothing free today, so return FULL
                                return Availability.FULL
                        # All events end today , so check for the start time of next day
                        # if there is a 12 hour window, there is time for an event
                        posstime = nextlist[0][0].hour + 24 - mystart
                        if (posstime >= 12):
                            return Availability.LOW
                        else:
                            return Availability.FULL

                    else:
                        # check, when the event from the prev day ended, depending on when, there might be no time left
                        posstime = nextlist[0][0].hour + 24 - lasteventhour
                        if (posstime >= 12):
                            return Availability.LOW
                        else:
                            return Availability.FULL

                else:
                    # start at 8 and next has event
                    mystart = 8
                    if (mylist):
                        for x in mylist:
                            timedif = x[0].hour - mystart
                            if (timedif >= 12):
                                # found a free timespot
                                return Availability.LOW
                            mystart = x[1].hour
                            if (x[1].day != date.day):
                                # goes into next day and nothing free today, so return FULL
                                return Availability.FULL
                        # All events end today , so check for the start time of next day
                        # if there is a 12 hour window, there is time for an event
                        posstime = nextlist[0][0].hour + 24 - mystart
                        if (posstime >= 12):
                            return Availability.LOW
                        else:
                            return Availability.FULL

                    else:
                        # next day has an event, so we can't book everyting
                        # even if today is free
                        return Availability.LOW

            else:
                if (intotoday):
                    # from prev and next has no event
                    # start the counting at the first free time
                    # 8 or the end of the event from the prev day, whatever is later
                    mystart = max(lasteventhour, 8)
                    if (mylist):
                        for x in mylist:
                            timedif = x[0].hour - mystart
                            if (timedif >= 12):
                                # found a free timespot
                                return Availability.LOW
                            mystart = x[1].hour
                            if (x[1].day != date.day):
                                # goes into next day and nothing free today, so return FULL
                                return Availability.FULL
                        # All events end today , so if the last ends before 24 o'clock, there is still time.
                        # If it ends at 24 o'clock, the day is full
                        if (mylist[-1][1].hour < 24):
                            return Availability.LOW
                        else:
                            return Availability.FULL

                    else:
                        # check, when the event from the prev day ended, depending on when, there might be no time left
                        if (lasteventhour <= 8):
                            return Availability.FREE
                        else:
                            # after 8, so some time blocked
                            # booking will still always be possible (nothing next day)
                            return Availability.LOW

                else:
                    # neither from prev day, nor next day
                    mystart = 8
                    if (mylist):
                        for x in mylist:
                            timedif = x[0].hour - mystart
                            if (timedif >= 12):
                                # found a free timespot
                                return Availability.LOW
                            mystart = x[1].hour
                            if (x[1].day != date.day):
                                # goes into next day and nothing free today, so return FULL
                                return Availability.FULL
                        # All events end today , so if the last ends before 24 o'clock, there is still time.
                        # If it ends at 24 o'clock, the day is full
                        if (mylist[-1][1].hour < 24):
                            return Availability.LOW
                        else:
                            return Availability.FULL

                    else:
                        return Availability.FREE
        else:
            # sunday
            if (intotoday):
                # events from saturday reach into today
                if (mylist):
                    mystart = max(8, lasteventhour)
                    for x in mylist:
                        timedif = x[0].hour - mystart
                        if (timedif >= 12):
                            # found a free timespot
                            return Availability.LOW
                        mystart = x[1].hour
                        if (x[1].day != date.day):
                            # goes into next day and nothing free today, so return FULL
                            return Availability.FULL
                    # check if it ends before 20 o'clock (last possible booking on sunday)
                    # if not, return full
                    if (mylist[-1][1].hour <= 20):
                        return Availability.LOW
                    else:
                        return Availability.FULL


                else:
                    # check, when the event from the prev day ended, depending on when, there might be no time left
                    if (lasteventhour <= 8):
                        return Availability.FREE
                    else:
                        # after 8, so some time blocked
                        # booking will still always be possible (nothing next day)
                        return Availability.LOW

            else:
                # no events from saturday
                if (mylist):
                    mystart = 8
                    for x in mylist:
                        timedif = x[0].hour - mystart
                        if (timedif >= 12):
                            # found a free timespot
                            return Availability.LOW
                        mystart = x[1].hour
                        if (x[1].day != date.day):
                            # goes into next day and nothing free today, so return FULL
                            return Availability.FULL
                    if (mylist[-1][1].hour <= 20):
                        return Availability.LOW
                    else:
                        return Availability.FULL

                else:
                    return Availability.FREE


def timeslot_available(start_time_to_check, end_time_to_check):
    """
    Check whether a timeslot is still bookable
    :param start_time_to_check: The start datetime of the timeslot
    :param end_time_to_check:  The end datetime of the timeslot
    :return: Boolean indicating whether the timeslot is available
    """
    # We allow overlap of one second to allow bookings from e.g. 14-17 and 17-20
    start_time_to_check = start_time_to_check + timedelta(seconds=1)
    end_time_to_check = end_time_to_check - timedelta(seconds=1)

    # Retrieve all events that interfere with the desired timeslot
    events = Event.objects.filter(Q(start_datetime__lte=start_time_to_check, end_datetime__gte=start_time_to_check)
                                  | Q(start_datetime__lte=end_time_to_check, end_datetime__gte=end_time_to_check)
                                  | Q(start_datetime__lte=start_time_to_check, end_datetime__gte=end_time_to_check)
                                  | Q(start_datetime__lte=end_time_to_check, start_datetime__gte=start_time_to_check)
                                  )

    if events:
        return False
    else:
        return True


def calculate_price(start_date, student, duration, number_people, end_datetime, refrigerator):
    """
    Calculate and return the price for given information
    :param start_date: Date object of the start
    :param student: Boolean indicating whether the student discount is applied
    :param duration: Duration of the booking as a integer
    :param number_people: Number of participating people as a integer
    :param end_datetime: Datetime object of the end
    :param refrigerator: Boolean indicating whether the refrigerator is needed
    :return: Price as a integer
    """
    # Check if day is a weekday
    day_type = get_day_type(start_date)

    # Check customer status
    if student:
        customer_status = 'Student'
    else:
        customer_status = 'noStudent'

    # Check duration
    if duration <= 3:
        duration_str = '3h'
    elif duration <= 6:
        duration_str = '6h'
    elif duration <= 12:
        duration_str = '12h'
    elif duration <= 24:
        duration_str = '24h'
    else:
        ValueError('Invalid duration')

    # Check persons
    if number_people <= 50:
        persons = 'under50'
    else:
        persons = 'over50'

    if day_type == 'WEEKDAY':
        subtotal = PriceEntry.objects.get(title='Week ' + persons + ' ' + customer_status + ' ' + duration_str).text
    else:
        subtotal = PriceEntry.objects.get(title='Weekend ' + customer_status + ' ' + duration_str).text

    # From 22h-8h on weekdays, there is a toilet fee
    if day_type == 'WEEKDAY' and (end_datetime.time() > dt.time(22, 0, 0)
                                  or end_datetime.time() < dt.time(8, 0, 0)):
        subtotal += PriceEntry.objects.get(title='Toilet Cleaning').text

    if day_type == 'WEEKEND':
        subtotal += PriceEntry.objects.get(title='Cleaning ' + customer_status).text

    return subtotal


def get_day_type(day_date):
    """
    Determine whether the given date is a weekday or weekend day.
    :param day_date: Date to check
    :return: String indicating the day type
    """
    if day_date.weekday() < 5:
        day_type = 'WEEKDAY'
    else:
        day_type = 'WEEKEND'
    return day_type


def str_to_bool(s):
    """Converts a human readable textual representation of a Boolean to a Boolean"""
    if s == 'yes':
        return True
    elif s == 'no':
        return False
    else:
        raise ValueError


class CancelledBooking(models.Model):
    """ Class represents a cancelled Event """
    start_datetime = models.DateTimeField(_('Startzeit'), default='', editable=False)

    end_datetime = models.DateTimeField(_('Endzeit'), default='', editable=False)

    booking_time = models.DateTimeField(_('Zeitpunkt der Buchung'), default='', editable=False)

    cancellation_time = models.DateTimeField(_('Zeitpunkt der Stornierung'), default=timezone.now, editable=False)

    author = models.ForeignKey(User, default=None, on_delete=models.PROTECT, editable=False)

    rent = models.IntegerField(_("Miete"), default=0, editable=False)

    rent_was_paid = models.BooleanField(_('hat der Kunde die Miete bereits gezahlt'), default=False, editable=False)

    rent_has_to_be_paid = models.BooleanField(_('die Miete muss zurückgezahlt werden'), default=False, editable=False)

    rent_paid_back = models.BooleanField(_('Rückzahlung der Miete erfolgt'), default=False, editable=True)

    def __str__(self):
        return 'Cancelled Booking from {}'.format(self.start_datetime.date())

    @classmethod
    def create(cls, event_to_cancel):
        """
        Create a new instance of the CancelledBooking class
        and fill its field based on the given Booking object
        :param event_to_cancel:  The Booking which will be deleted
        :return: New Instance of the CancelledBooking class
        """
        if event_to_cancel is None:
            raise Exception('given Booking has not to be none')
        if not isinstance(event_to_cancel, Booking):
            raise Exception('given object has an instance of Booking')

        # receive all needed data from the event that will be cancelled
        start = event_to_cancel.start_datetime
        end = event_to_cancel.end_datetime
        booking = event_to_cancel.booking_time
        author = event_to_cancel.author
        # calculate the rent the user payed/would have payed
        rent = event_to_cancel.calculate_price_event()
        # check if the rent was already payed
        rent_was_paid = event_to_cancel.rent_paid
        # calculate if the User will get his payment back
        today = datetime.today()
        diff = (start - today).days
        rent_has_to_be_paid = True
        if diff < 5:
            rent_has_to_be_paid = False
            event_to_cancel.send_cancellation_email_customer(free=False)
        else:
            event_to_cancel.send_cancellation_email_customer(free=True)

        # send mails to staff
        event_to_cancel.send_cancellation_email_admin()
        event_to_cancel.send_cancellation_email_caretaker()
        event_to_cancel.send_cancellation_email_cleaning()
        event_to_cancel.send_cancellation_email_tutor()

        cbooking = cls(start_datetime=start, end_datetime=end, booking_time=booking, author=author,
                       rent=rent, rent_was_paid=rent_was_paid, rent_has_to_be_paid=rent_has_to_be_paid)
        return cbooking


#this method is used to calculate the weekly dates that are between the parameters start and end
def calculate_weekly_dates(start, end):

    # validation of input dates and times
    tmp2 = int(end.strftime("%d")) - int(start.strftime("%d"))
    if (tmp2 % 7) != 0:
        raise ValidationError("Erster und letzter Termin müssen am gleichen Wochentag sein.")

    if start >= end:
        raise ValidationError("Erster Termin darf nicht größer oder gleich dem letzten Termin sein.")

    dur = (end - start).total_seconds() / 3600
    if (dur % 1) != 0:
        raise ValidationError("Die Dauer des Termins darf nur ganze Stunden betragen (1 Std., 2 Std., ...).")

    if start.strftime("%H:%M") == end.strftime("%H:%M"):
        raise ValidationError("Start- und Endzeit dürfen nicht gleich sein.")

    event_dates = list()
    start_event = start
    end_event = dt.datetime(start.year, start.month, start.day, end.hour, end.minute)

    while start_event <= end:
        event_dates.append((start_event, end_event))
        start_event += dt.timedelta(days=7)
        end_event += dt.timedelta(days=7)

    return event_dates


class WeeklyBooking(models.Model):
    # Class represents a weekly bookings
    start_datetime = models.DateTimeField(_('erster Termin'), default=tz.now)
    end_datetime = models.DateTimeField(_('letzter Termin'), default=tz.now)
    exception_first = models.DateField(_('Erste Ausnahme'), blank=True, null=True)
    exception_second = models.DateField(_('Zweite Ausnahme'), blank=True, null=True)
    exception_third = models.DateField(_('Dritte Ausnahme'), blank=True, null=True)
    exception_forth = models.DateField(_('Vierte Ausnahme'), blank=True, null=True)
    exception_fifth = models.DateField(_('Fünfte Ausnahme'), blank=True, null=True)

    def save(self, *args, **kwargs):
        """Create a new instance of the WeeklyBooking class
        but only if it does not collide with any other events
        :param start: start date and time of the weekly meeting
                end: end date and time of the weekly meeting
        :return: New Instance of the WeeklyBooking class"""

        weekly_dates = calculate_weekly_dates(self.start_datetime, self.end_datetime)

        # if there are no collisions create blockers for the weekly meetings
        super().save(*args, **kwargs)

        for wd in weekly_dates:
            tmp = dt.date(wd[0].year, wd[0].month, wd[0].day)
            if not (self.exception_first == tmp) and not (self.exception_second == tmp) and not (
                    self.exception_third == tmp) \
                    and not (self.exception_forth == tmp) and not (self.exception_fifth == tmp):
                dur = int((wd[1] - wd[0]).total_seconds() / 3600)
                blocker = Blocker(date=wd[0], start_time=wd[1], duration=dur)
                blocker.save()



class WeeklyBookingAdminForm(forms.ModelForm):
#this class represents the form that the admin uses to create a new weekly meeting

    #this methods cleans the admin's input
    def clean(self, ):

        super(WeeklyBookingAdminForm, self).clean()

        start_datetime = self.cleaned_data.get('start_datetime')
        end_datetime = self.cleaned_data.get('end_datetime')

        weekly_dates = calculate_weekly_dates(start_datetime, end_datetime)
        collisions = list()

        # check if one of the dates collides with an existing event
        for d in weekly_dates:
            if not (timeslot_available(d[0], d[1])):
                collisions.append(d[0])

        # if there are collisions show to the admin which on which dates and do not create a weekly meeting
        if len(collisions) != 0:
            collisions_string = ""
            for collision in collisions:
                collisions_string += collision.strftime("[%d.%m.%Y] \n")
            raise forms.ValidationError(
                "Es konnte keine Buchung erstellt werden, da es an folgenden Daten zu Kollisionen " +
                "mit bereits existierenden Buchungen (oder Blocker) gibt: \n" + collisions_string +
                ". Wenn Sie die Buchung trotzdem erstellen möchten, können Sie entweder die Buchungen an den obenen angegebenen Termin(en) " +
                "löschen oder die angegebenen Daten als Ausnahmen angeben, dann würden für alle anderen Tage außer diese Blocker erstellt werden.")

        return self.cleaned_data
