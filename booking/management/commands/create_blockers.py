from django.core.management.base import BaseCommand
from booking.models import Blocker
from datetime import date, time, timedelta
from booking.models import get_day_type


class Command(BaseCommand):
    help = 'create blockers for the next 5 years on each weekday 8-16h'

    def handle(self, *args, **options):
        for current_date in (date.today() + timedelta(n) for n in range(5 * 365)):
            if get_day_type(current_date) == 'WEEKDAY':
                obj, created = Blocker.objects.get_or_create(
                    date=current_date,
                    start_time=time(8),
                    duration=8
                )
