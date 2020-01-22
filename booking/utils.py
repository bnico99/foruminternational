from datetime import date
from dateutil.relativedelta import relativedelta
from calendar import HTMLCalendar
from django.utils.translation import get_language
from .models import get_date_availability


class Calendar(HTMLCalendar):

    def __init__(self, year=None, month=None, locale=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def formatday(self, day, dayyear, daymonth):
        """
        Returns a formatted day.
        """
        if day != 0:
            datum = date(int(dayyear), int(daymonth), int(day))
            av = get_date_availability(datum)
            bcolor = self.get_av_color(av)
            if (datum <= date.today()) | six_month_ahead(datum):
                return f'''<td valign="top"> <div  style="text-decoration:none; color:white; background-color:grey"> <span class='date'>{day}</span></div> </td>'''
            else:
                return f'''<td valign="top"> <a href="?datum={datum}#dayselected"  style="text-decoration:none; color:white; background-color:{bcolor}"> <span class='date'>{day}</span></a></td>'''
        return '<td></td>'

    def get_av_color(self, av):
        """
        returns the color of the availability (green, yellow, red)
        :param av: availability
        :return: the color as string
        """
        if (av == av.FREE):
            bcolor = "green"
        elif (av == av.LOW):
            bcolor = "rgb(204,204,0)"
        else:
            bcolor = "red"
        return bcolor

    def formatweek(self, theweek, weekyear, weekmonth):
        """
        Return a complete week as a table row.
        """
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, weekyear, weekmonth)
        return f'<tr> {week} </tr>'

    def formatweekday(self, day):
        """
        Return a weekday name as a table header.
        """
        return '<th class="%s">%s</th>' % (
            self.cssclasses_weekday_head[day], get_weekdayname(day))

    def formatmonth(self, withyear=True):
        """
        Return a formatted month as a table.
        """
        cal = f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, self.year, self.month)}\n'
        return cal

    def formatmonthname(self, theyear, themonth, withyear=True):
        """
        Return a month name as a table row.
        """
        monthname = get_monthname(themonth)
        if withyear:
            s = '%s %s' % (monthname, theyear)
        else:
            s = '%s' % monthname
        return '<tr><th colspan="7" class="%s">%s</th></tr>' % (
            self.cssclass_month_head, s)


def get_monthname(themonth):
    """
    Return a month name in the respective language.
    :param themonth: the number of the month
    :return: month name as string
    """
    lang = get_language()
    month_german = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober",
                    "November", "Dezember"]
    month_english = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                     "November", "December"]
    month_french = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre",
                    "Novembre", "Décembre"]
    if "de" == lang:
        return month_german[themonth - 1]
    elif "en" == lang:
        return month_english[themonth - 1]
    elif "fr" == lang:
        return month_french[themonth - 1]


def get_weekdayname(day):
    """
    Return an abbreviated weekday name in the respective language.
    :param day: integer between 0 and 6 for respective weekday number
    :return: abbreviated weekday name as string
    """
    lang = get_language()
    week_german = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
    week_english = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    week_french = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
    if "de" == lang:
        return week_german[day]
    elif "en" == lang:
        return week_english[day]
    elif "fr" == lang:
        return week_french[day]


def six_month_ahead(datum):
    """
    Check whether the date given is (more than) six month ahead from today
    :param datum: the date to check
    :return: bool
    """
    return datum >= date.today() + relativedelta(months=+6)
