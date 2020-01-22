from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

from .models import Profile
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
import re
import datetime


class UserSignUpForm(UserCreationForm):
    # create a list of title choices
    title_choices = [
        ("Herr", _("Herr")),
        ("Frau", _("Frau")),
    ]

    # get the current year
    now = datetime.datetime.now()
    current_year = now.year

    # create a list of birthday year choices
    years_int = list(range(current_year - 120, current_year + 1))
    years_int.reverse()
    BIRTH_YEAR_CHOICES = [str(i) for i in years_int]

    title = forms.ChoiceField(required=True, label=_("Anrede"), choices=title_choices)
    first_name = forms.CharField(max_length=30, required=True, label=_("Vorname"))
    last_name = forms.CharField(max_length=30, required=True, label=_("Nachname"))
    email = forms.EmailField(max_length=40, required=True,
                             help_text=_('Bitte geben Sie eine korrekte E-Mail-Adresse an.'),
                             label=_("Email-Adresse"))
    zip_code = forms.CharField(max_length=5, required=True, label=_("PLZ"))
    city = forms.CharField(max_length=30, required=True, label=_("Ort"))
    street = forms.CharField(max_length=30, required=True, label=_("Straße"))
    house_number = forms.CharField(max_length=10, required=True, label=_('Hausnummer'))
    phone = forms.CharField(max_length=15, required=True, label=_('Telefonnummer'))
    date_of_birth = forms.DateField(required=True, label=_('Geburtsdatum'),
                                    widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))
    data_privacy = forms.BooleanField(required=True, label=mark_safe('<a href="https://www.studentenwerk-saarland.de/de/footer/Datenschutz" target="_blank" class=""> Datenschutzerklärung</a> bestätigen'))
    class Meta:
        model = User
        fields = ('title', 'username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'date_of_birth',
                  'zip_code', 'city', 'street', 'house_number', 'phone', 'data_privacy')

    # this function will be used for the validation of the registration form
    def clean(self):
        # fetch data from form
        super(UserSignUpForm, self).clean()

        title = self.cleaned_data.get('title')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')
        zip_code = self.cleaned_data.get('zip_code')
        city = self.cleaned_data.get('city')
        street = self.cleaned_data.get('street')
        house_number = self.cleaned_data.get('house_number')
        phone = self.cleaned_data.get('phone')
        date_of_birth = self.cleaned_data.get('date_of_birth')
        data_privacy = self.cleaned_data.get('data_privacy')

        validate_input_registration(title, first_name, last_name, email, zip_code, city, street, house_number, phone,
                                    date_of_birth, data_privacy)

        return self.cleaned_data


def validate_input_registration(title, first_name, last_name, email, zip_code, city, street, house_number, phone,
                                date_of_birth, data_privacy):

    if not data_privacy == True:
        raise forms.ValidationError(_("Bitte akzeptieren Sie die Datenschutzerklärung um fortzufahren."))

    if not (title == "Herr" or title == "Frau"):
        raise forms.ValidationError(_("Der eingegebene Titel ist nicht valide."))

    if not re.match(
            r"^[A-ZÀÈÌÒÙÁÉÍÓÚÃÑÕÝÄËÏÖÜŸÇŒØÅÆÞÐ][a-zàèìòùáéíóúýãñõâêîôûäëïöüçœßøåæþðA-ZÀÈÌÒÙÁÉÍÓÚÃÑÕÝÄËÏÖÜŸÇŒØÅÆÞÐ \-\s\']*[a-zàèìòùáéíóúýãñõâêîôûäëïöüçœßøåæþð]$",
            first_name):
        raise forms.ValidationError(_("Der eingegebene Vorname ist nicht valide.\n" +
                                    "Vornamen müssen mit einem Großbuchstaben beginnen und dürfen nur aus Buchstaben und den folgenden Symbolen bestehen -,'."))

    if not re.match(
            r"^[a-zàèìòùáéíóúýãñõâêîôûäëïöüçœßøåæþðA-ZÀÈÌÒÙÁÉÍÓÚÃÑÕÝÄËÏÖÜŸÇŒØÅÆÞÐ][a-zàèìòùáéíóúýãñõâêîôûäëïöüçœßøåæþðA-ZÀÈÌÒÙÁÉÍÓÚÃÑÕÝÄËÏÖÜŸÇŒØÅÆÞÐ \-\s\']*[a-zàèìòùáéíóúýãñõâêîôûäëïöüçœßøåæþð]$",
            last_name):
        raise forms.ValidationError(_("Der eingegebene Nachname ist nicht valide.\n"+
                                    "Nachnamen müssen mit einem Großbuchstaben beginnen und dürfen nur aus Buchstaben und den folgenden Symbolen bestehen -,'."))

    if User.objects.filter(email=email).exists():
        raise forms.ValidationError(_("Es existiert bereits ein Account zu dieser E-Mail-Adresse."))

    if not re.match(r".*[@].*[.].*", email):
        raise forms.ValidationError(_("Der eingegebene E-Mail-Adresse ist nicht valide."))

    if zip_code:
        if not re.match(r"^[0-9][0-9][0-9][0-9][0-9]$", zip_code):
            raise forms.ValidationError(_("Die eingegebene Postleitzahl ist nicht valide."))

    if not re.match(
            r"^[A-ZÀÈÌÒÙÁÉÍÓÚÃÑÕÝÄËÏÖÜŸÇŒØÅÆÞÐ][a-zàèìòùáéíóúýãñõâêîôûäëïöüçœßøåæþðA-ZÀÈÌÒÙÁÉÍÓÚÃÑÕÝÄËÏÖÜŸÇŒØÅÆÞÐ \-\s\'\.]*[a-zàèìòùáéíóúýãñõâêîôûäëïöüçœßøåæþð]$",
            city):
        raise forms.ValidationError(_("Die eingegebene Stadt ist nicht valide.\n"+
                                    "Städtenamen müssen mit einem Großbuchstaben beginnen und dürfen nur aus Buchstaben und den folgenden Symbolen bestehen .,-,'."))

    if not re.match(
            r"^[A-ZÀÈÌÒÙÁÉÍÓÚÃÑÕÝÄËÏÖÜŸÇŒØÅÆÞÐ][a-zàèìòùáéíóúýãñõâêîôûäëïöüçœßøåæþðA-ZÀÈÌÒÙÁÉÍÓÚÃÑÕÝÄËÏÖÜŸÇŒØÅÆÞÐ \-\s\'\.]*[a-zàèìòùáéíóúýãñõâêîôûäëïöüçœßøåæþð \.]$",
            street):
        raise forms.ValidationError(_("Der eingegebene Straßenname ist nicht valide.\n"+
                                    "Straßennamen müssen mit einem Großbuchstaben beginnen und dürfen nur aus Buchstaben und den folgenden Symbolen bestehen .,-,'."))

    if not re.match(r"^[1-9][0-9]*[a-z]?", house_number):
        raise forms.ValidationError(_("Die eingegebene Hausnummer ist nicht valide.\n"+
                                    "Hausnummern müssen mit einer Zahl zwischen 1-9 beginnen und dürfen nur aus Buchstaben und Zahlen bestehen."))

    if not re.match(r"^[0-9+][0-9/ \s][0-9/ \s][0-9/ \s]*[0-9]$", phone):
        raise forms.ValidationError(_("Die eingegebene Telefonnummer ist nicht valide. Telefonnummer müssen mit einer Zahl oder dem Zeichen + beginnen." +
                                    "Sie dürfen nur aus Zahlen und den Zeichen + und / bestehen."))

    if date_of_birth.year > datetime.date.today().year or date_of_birth.year < 1900:
        raise forms.ValidationError(_("Das eingegebene Geburtsjahr ist nicht valide."))

    if date_of_birth.month >= 13 or date_of_birth.month < 1:
        raise forms.ValidationError(_("Der eingegebene Geburtsmonat ist nicht valide."))

    if date_of_birth.month >= 32 or date_of_birth.month < 1:
        raise forms.ValidationError(_("Der eingegebene Geburtstag ist nicht valide."))



class UserProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['username']
