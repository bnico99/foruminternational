from django.core.exceptions import ValidationError
from django.forms import Textarea

from django.forms import ModelForm
from django.utils.datetime_safe import datetime
from dateutil.relativedelta import relativedelta
from django.utils.translation import gettext_lazy as _

import datetime as dt

from booking.models import Booking, timeslot_available, get_day_type


class BookingForm(ModelForm):
    class Meta:
        model = Booking
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
            'occasion': Textarea(attrs={'rows': '3'})
        }
        fields = ['date', 'start_time', 'duration', 'student', 'number_people', 'refrigerator', 'occasion']

    # this function will be used for the validation
    def clean(self):
        # fetch data from form
        super(BookingForm, self).clean()

        start_date = self.cleaned_data.get('date')
        start_time = self.cleaned_data.get('start_time')
        duration = self.cleaned_data.get('duration')
        student = self.cleaned_data.get('student')
        number_people = self.cleaned_data.get('number_people')
        refrigerator = self.cleaned_data.get('refrigerator')
        occasion = self.cleaned_data.get('occasion')

        validate_input(start_date, start_time, duration, student, number_people, refrigerator, occasion)

        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)

        self.fields['date'].widget.attrs['readonly'] = True
        self.fields['date'].help_text = None
        self.fields['start_time'].widget.attrs['readonly'] = True
        self.fields['start_time'].help_text = None
        self.fields['duration'].widget.attrs['readonly'] = True
        self.fields['duration'].help_text = None


def validate_input(start_date, start_time, duration, student, number_people, refrigerator, occasion):
    start_datetime = datetime.combine(start_date, start_time)
    end_datetime = start_datetime + dt.timedelta(hours=duration)
    today = datetime.today()
    if start_datetime < today:
        raise ValidationError(_('You cant book events in the past'), 'unavailable_timeslot')
    today += relativedelta(months=+6)
    if start_datetime > today:
        raise ValidationError(_('You cant book so far in the future'), 'unavailable_timeslot')
    if not timeslot_available(start_datetime, end_datetime):
        raise ValidationError(_('Es gibt bereits eine Buchung zu diesem Zeitpunkt.'), 'unavailable_timeslot')

    day_type = get_day_type(start_date)
    if (day_type == 'WEEKDAY') and duration not in [3, 6, 12]:
        raise ValidationError(_('An Wochentagen ist nur eine 3-,6- oder 12-stündige Buchung möglich.'),
                              'invalid_duration')
    elif (day_type == 'WEEKEND') and duration not in [12, 24]:
        raise ValidationError(_('An Wochenenden ist nur eine 12- oder 24-stündige Buchung möglich.'),
                              'invalid_duration')

    if start_time < dt.time(8, 0):
        raise ValidationError(_('Eine Buchung ist erst ab 8 Uhr (Mo-Fr) bzw. 16 Uhr (Sa-So) möglich.'))

    if start_time.minute != 0:
        raise ValidationError(_('Buchungen können nur zur vollen Stunde beginnen.'), 'invalid_starttime')

    if number_people <= 0:
        raise ValidationError(_('Die Anzahl erscheinender Personen muss größer als 0 sein.'), 'invalid_people_num')

    if student != 'yes' and student != 'no':
        raise ValidationError(_('Ungültige Eingabe bei Studentenfrage.'), 'invalid_student_input')

    if refrigerator != 'yes' and refrigerator != 'no':
        raise ValidationError(_('Ungültige Eingabe bei Kühlschrankfrage.'), 'invalid_refrigerator_input')

    if occasion == '':
        raise ValidationError(_('Das Feld zum Anlass darf nicht leer sein.'), 'empty_occasion')
