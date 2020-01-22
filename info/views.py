from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from django.urls import reverse
from user_account.models import Profile
from .models import FAQEntry, InfoText, FAQEntryFR, FAQEntryEN, PriceEntry
from django.utils.translation import get_language


def home(request):
    """
    the view which represents the Home page
    :param request: request used to call website
    :return: the Home Page
    """
    lang = get_language()

    # based on selected language load the correct home text
    if "fr" == lang:
        home_site = get_object_or_404(InfoText, title="HomeFR")
    elif "en" == lang:
        home_site = get_object_or_404(InfoText, title="HomeEN")
    else:
        home_site = get_object_or_404(InfoText, title="Home")
    return render(request, "info/home.html", {'home': home_site})


# reading the questions and answers from the database
def faq(request):
    """
    the view which represents the info site
    :param request: request used to call website
    :return: the info page including FAQ
    """
    lang = get_language()
    inspection = request.GET.get('inspection', '0')

    # choose FAQ entrys based on language chosen
    if "fr" == lang:
        faq_entries = FAQEntryFR.objects.all()
    elif "en" == lang:
        faq_entries = FAQEntryEN.objects.all()
    else:
        faq_entries = FAQEntry.objects.all()

    context = {
        'faq_entries': faq_entries,

        'WSunder503h': get_object_or_404(PriceEntry, title="Week under50 Student 3h"),
        'WSunder506h': get_object_or_404(PriceEntry, title="Week under50 Student 6h"),
        'WSunder509h': get_object_or_404(PriceEntry, title="Week under50 Student 12h"),

        'WSover503h': get_object_or_404(PriceEntry, title="Week over50 Student 3h"),
        'WSover506h': get_object_or_404(PriceEntry, title="Week over50 Student 6h"),
        'WSover509h': get_object_or_404(PriceEntry, title="Week over50 Student 12h"),

        'WnSunder503h': get_object_or_404(PriceEntry, title="Week under50 noStudent 3h"),
        'WnSunder506h': get_object_or_404(PriceEntry, title="Week under50 noStudent 6h"),
        'WnSunder509h': get_object_or_404(PriceEntry, title="Week under50 noStudent 12h"),

        'WnSover503h': get_object_or_404(PriceEntry, title="Week over50 noStudent 3h"),
        'WnSover506h': get_object_or_404(PriceEntry, title="Week over50 noStudent 6h"),
        'WnSover509h': get_object_or_404(PriceEntry, title="Week over50 noStudent 12h"),

        'WES12h': get_object_or_404(PriceEntry, title="Weekend Student 12h"),
        'WES24h': get_object_or_404(PriceEntry, title="Weekend Student 24h"),

        'WEnS12h': get_object_or_404(PriceEntry, title="Weekend noStudent 12h"),
        'WEnS24h': get_object_or_404(PriceEntry, title="Weekend noStudent 24h"),

        'CleaningStudent': get_object_or_404(PriceEntry, title="Cleaning Student"),
        'CleaningNoStudent': get_object_or_404(PriceEntry, title="Cleaning noStudent"),
        'ToiletCleaning': get_object_or_404(PriceEntry, title="Toilet Cleaning"),

        'inspection': inspection,
    }

    if request.POST:
        request_inspection(request)
        return HttpResponseRedirect(reverse('info:confirm'))

        # return render(request, 'info/request_visit.html')

    return render(request, 'info/faq.html', context)


def request_inspection(request):
    """
    function used to request an inspection of the room
    :param request: request used to call the function
    :return: sends all needed emails to the user and the tutor
    """
    user = request.user
    pk = user.pk
    user = Profile.objects.get(pk=pk)
    user.send_visit_email_tutor()


def visit_confirm(request):
    return render(request, 'info/request_visit.html')
