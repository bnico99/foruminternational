from django.core.management.base import BaseCommand, CommandError
from booking.models import Booking
import datetime as dt

class Command(BaseCommand):
    """name of the command: remind_customers.py
    this command will send a reminder email to all the customers who have booked the room and have not paid the rent yet,
    although there are just 3 days left to the event date
    this command should be run every day"""

    help = 'reminds the customer to pay the rent'

    def handle(self, *args, **options):

        #get today's date
        today = dt.date.today()

        #loop through all the bookings and check if there are exactly three days remaining to the booking and the rent is not paid
        for booking in Booking.objects.all():
            if (booking.date - dt.timedelta(days=3)) == today and not booking.rent_paid:
                booking.send_reminder_email_customer() #send email to customer if this is the case

