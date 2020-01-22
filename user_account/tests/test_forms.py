from django.test import TestCase
from user_account.forms import UserSignUpForm


class TestForms(TestCase):

    def test_valid_form(self):
        form = UserSignUpForm(data={
            'title': 'Herr',
            'first_name': 'Max',
            'last_name': 'Musterman',
            'date_of_birth': '1990-1-1',
            'email': 'max@mustermann.com',
            'password1': 'DieTPwFSE1920%%',
            'password2': 'DieTPwFSE1920%%',
            'zip_code': '12345',
            'city': 'Saarbruecken',
            'street': 'Schlossalee',
            'house_number': '13',
            'phone': '152212345667',
            'username': 'MAXMU',
            'data_privacy': 'True'
        })
        self.assertTrue(form.is_valid(), form.errors)

    def test_signup_form_valid_data_special_accepted_last_name(self):
        form = UserSignUpForm(data={
            'title': 'Herr',
            'first_name': 'Max',
            'last_name': 'O\'Musterman',
            'date_of_birth': '1990-1-1',
            'email': 'max@mustermann.com',
            'password1': 'DieTPwFSE1920%%',
            'password2': 'DieTPwFSE1920%%',
            'zip_code': '12345',
            'city': 'Saarbruecken',
            'street': 'Schlossalee',
            'house_number': '13',
            'phone': '0152212345667',
            'username': 'MAXMU',
            'data_privacy': 'True'
        })

        self.assertTrue(form.is_valid(), form.errors)

    def test_signup_form_valid_data_not_accepted_last_name(self):
        form = UserSignUpForm(data={
            'title': 'Herr',
            'first_name': 'Max',
            'last_name': 'O\'Musterman123',
            'date_of_birth': '1990-1-1',
            'email': 'max@mustermann.com',
            'password1': 'DieTPwFSE1920%%',
            'password2': 'DieTPwFSE1920%%',
            'zip_code': '12345',
            'city': 'Saarbruecken',
            'street': 'Schlossalee',
            'house_number': '13',
            'phone': '0152212345667',
            'username': 'MAXMU',
            'data_privacy': 'True'
        })

        self.assertFalse(form.is_valid(), form.errors)

    def test_signup_form_valid_data_special_accepted_last_name_2(self):
        form = UserSignUpForm(data={
            'title': 'Herr',
            'first_name': 'Max',
            'last_name': 'Maxémçäüößatrin-Katrin Lena',
            'date_of_birth': '1990-1-1',
            'email': 'max@mustermann.com',
            'password1': 'DieTPwFSE1920%%',
            'password2': 'DieTPwFSE1920%%',
            'zip_code': '12345',
            'city': 'Saarbruecken',
            'street': 'Schlossalee',
            'house_number': '13',
            'phone': '0152212345667',
            'username': 'MAXMU',
            'data_privacy': 'True'
        })

        self.assertTrue(form.is_valid(), form.errors)

    def test_signup_form_valid_data_special_accepted_first_name(self):
        form = UserSignUpForm(data={
            'title': 'Herr',
            'first_name': 'Maxémçäüößatrin-Katrin Lena',
            'last_name': 'Musterman',
            'date_of_birth': '1990-1-1',
            'email': 'max@mustermann.com',
            'password1': 'DieTPwFSE1920%%',
            'password2': 'DieTPwFSE1920%%',
            'zip_code': '12345',
            'city': 'Saarbruecken',
            'street': 'Schlossalee',
            'house_number': '13',
            'phone': '0152212345667',
            'username': 'MAXMU',
            'data_privacy': 'True'
        })

        self.assertTrue(form.is_valid(), form.errors)

    def test_signup_form_valid_data_not_accepted_first_name(self):
        form = UserSignUpForm(data={
            'title': 'Herr',
            'first_name': 'M. Johannes',
            'last_name': 'Musterman',
            'date_of_birth': '1990-1-1',
            'email': 'max@mustermann.com',
            'password1': 'DieTPwFSE1920%%',
            'password2': 'DieTPwFSE1920%%',
            'zip_code': '12345',
            'city': 'Saarbruecken',
            'street': 'Schlossalee',
            'house_number': '13',
            'phone': '0152212345667',
            'username': 'MAXMU',
            'data_privacy': 'True'
        })

        self.assertFalse(form.is_valid(), form.errors)

    def test_signup_form_valid_data_special_house_number(self):
        form = UserSignUpForm(data={
            'title': 'Herr',
            'first_name': 'Max',
            'last_name': 'Musterman',
            'date_of_birth': '1990-1-1',
            'email': 'max@mustermann.com',
            'password1': 'DieTPwFSE1920%%',
            'password2': 'DieTPwFSE1920%%',
            'zip_code': '12345',
            'city': 'Saarbruecken',
            'street': 'Schlossalee',
            'house_number': '13b',
            'phone': '0152212345667',
            'username': 'MAXMU',
            'data_privacy': 'True'
        })
        self.assertTrue(form.is_valid(), form.errors)

    def test_signup_form_valid_data_house_number_beginning_zero(self):
        form = UserSignUpForm(data={
            'title': 'Herr',
            'first_name': 'Max',
            'last_name': 'Musterman',
            'date_of_birth': '1990-1-1',
            'email': 'max@mustermann.com',
            'password1': 'DieTPwFSE1920%%',
            'password2': 'DieTPwFSE1920%%',
            'zip_code': '12345',
            'city': 'Saarbruecken',
            'street': 'Schlossalee',
            'house_number': '013b',
            'phone': '0152212345667',
            'username': 'MAXMU',
            'data_privacy': 'True'
        })
        self.assertFalse(form.is_valid(), form.errors)

    def test_signup_form_valid_data_invalid_year(self):
        form = UserSignUpForm(data={
            'title': 'Herr',
            'first_name': 'Max',
            'last_name': 'Mustermann',
            'date_of_birth': '2021-1-1',
            'email': 'max@mustermann.com',
            'password1': 'DieTPwFSE1920%%',
            'password2': 'DieTPwFSE1920%%',
            'zip_code': '12345',
            'city': 'Saarbruecken',
            'street': 'Schlossalee',
            'house_number': '13',
            'phone': '0152212345667',
            'username': 'MAXMU',
            'data_privacy': 'True'
        })

        self.assertFalse(form.is_valid(), form.errors)

    def test_signup_form_negative_phone_number(self):
        form = UserSignUpForm(data={
            'title': 'Herr',
            'first_name': 'Max',
            'last_name': 'Musterman',
            'date_of_birth': '1990-1-1',
            'email': 'max@mustermann.com',
            'password1': 'DieTPwFSE1920%%',
            'password2': 'DieTPwFSE1920%%',
            'zip_code': '12345',
            'city': 'Saarbruecken',
            'street': 'Schlossalee',
            'house_number': '13',
            'phone': '-152212345667',
            'username': 'MAXMU',
            'data_privacy': 'True'
        })
        self.assertFalse(form.is_valid())

    def test_signup_form_negative_zip_code(self):
        form = UserSignUpForm(data={
            'title': 'Herr',
            'first_name': 'Max',
            'last_name': 'Musterman',
            'date_of_birth': '1990-1-1',
            'email': 'max@mustermann.com',
            'password1': 'DieTPwFSE1920%%',
            'password2': 'DieTPwFSE1920%%',
            'zip_code': '-12345',
            'city': 'Saarbruecken',
            'street': 'Schlossalee',
            'house_number': '13',
            'phone': '152212345667',
            'username': 'MAXMU',
            'data_privacy': 'True'
        })
        self.assertFalse(form.is_valid())

    def test_signup_form_negative_house_number(self):
        form = UserSignUpForm(data={
            'title': 'Herr',
            'first_name': 'Max',
            'last_name': 'Musterman',
            'date_of_birth': '1990-1-1',
            'email': 'max@mustermann.com',
            'password1': 'DieTPwFSE1920%%',
            'password2': 'DieTPwFSE1920%%',
            'zip_code': '12345',
            'city': 'Saarbruecken',
            'street': 'Schlossalee',
            'house_number': '-13',
            'phone': '152212345667',
            'username': 'MAXMU',
            'data_privacy': 'True'
        })
        self.assertFalse(form.is_valid())

    def test_signup_form_too_long_zip_code(self):
        form = UserSignUpForm(data={
            'title': 'Herr',
            'first_name': 'Max',
            'last_name': 'Musterman',
            'date_of_birth': '1990-1-1',
            'email': 'max@mustermann.com',
            'password1': 'DieTPwFSE1920%%',
            'password2': 'DieTPwFSE1920%%',
            'zip_code': '123456',
            'city': 'Saarbruecken',
            'street': 'Schlossalee',
            'house_number': '13',
            'phone': '152212345667',
            'username': 'MAXMU',
            'data_privacy': 'True'
        })
        self.assertFalse(form.is_valid())

    def test_signup_form_too_short_zip_code(self):
        form = UserSignUpForm(data={
            'title': 'Herr',
            'first_name': 'Max',
            'last_name': 'Musterman',
            'date_of_birth': '1990-1-1',
            'email': 'max@mustermann.com',
            'password1': 'DieTPwFSE1920%%',
            'password2': 'DieTPwFSE1920%%',
            'zip_code': '1234',
            'city': 'Saarbruecken',
            'street': 'Schlossalee',
            'house_number': '13',
            'phone': '152212345667',
            'username': 'MAXMU',
            'data_privacy': 'True'
        })
        self.assertFalse(form.is_valid())

    def test_signup_form_special_street_name(self):
        form = UserSignUpForm(data={
            'title': 'Herr',
            'first_name': 'Max',
            'last_name': 'Musterman',
            'date_of_birth': '1990-1-1',
            'email': 'max@mustermann.com',
            'password1': 'DieTPwFSE1920%%',
            'password2': 'DieTPwFSE1920%%',
            'zip_code': '12345',
            'city': 'Saarbruecken',
            'street': 'St.-Ingberterstr.',
            'house_number': '13',
            'phone': '152212345667',
            'username': 'MAXMU',
            'data_privacy': 'True'
        })
        self.assertTrue(form.is_valid())

    def test_signup_form_special_city_name(self):
        form = UserSignUpForm(data={
            'title': 'Herr',
            'first_name': 'Max',
            'last_name': 'Musterman',
            'date_of_birth': '1990-1-1',
            'email': 'max@mustermann.com',
            'password1': 'DieTPwFSE1920%%',
            'password2': 'DieTPwFSE1920%%',
            'zip_code': '12345',
            'city': 'St.Ingbert',
            'street': 'Mecklenburgring',
            'house_number': '13',
            'phone': '152212345667',
            'username': 'MAXMU',
            'data_privacy': 'True'
        })
        self.assertTrue(form.is_valid())

    def test_signup_form_too_short_phone(self):
        form = UserSignUpForm(data={
            'title': 'Herr',
            'first_name': 'Max',
            'last_name': 'Musterman',
            'date_of_birth': '1990-1-1',
            'email': 'max@mustermann.com',
            'password1': 'DieTPwFSE1920%%',
            'password2': 'DieTPwFSE1920%%',
            'zip_code': '12345',
            'city': 'St.Ingbert',
            'street': 'Mecklenburgring',
            'house_number': '13',
            'phone': '152',
            'username': 'MAXMU',
            'data_privacy': 'True'
        })
        self.assertFalse(form.is_valid())

    def test_signup_form_special_fist_name(self):
        form = UserSignUpForm(data={
            'title': 'Herr',
            'first_name': 'Ann-Katrin',
            'last_name': 'Musterman',
            'date_of_birth': '1990-1-1',
            'email': 'max@mustermann.com',
            'password1': 'DieTPwFSE1920%%',
            'password2': 'DieTPwFSE1920%%',
            'zip_code': '12345',
            'city': 'St.Ingbert',
            'street': 'Mecklenburgring',
            'house_number': '13',
            'phone': '152212345667',
            'username': 'MAXMU',
            'data_privacy': 'True'
        })
        self.assertTrue(form.is_valid())

    def test_signup_form_special_last_name(self):
        form = UserSignUpForm(data={
            'title': 'Herr',
            'first_name': 'Max',
            'last_name': 'Mustermann-Muster',
            'date_of_birth': '1990-1-1',
            'email': 'max@mustermann.com',
            'password1': 'DieTPwFSE1920%%',
            'password2': 'DieTPwFSE1920%%',
            'zip_code': '12345',
            'city': 'St.Ingbert',
            'street': 'Mecklenburgring',
            'house_number': '13',
            'phone': '152212345667',
            'username': 'MAXMU',
            'data_privacy': 'True'
        })
        self.assertTrue(form.is_valid())

    def test_signup_form_same_password_username(self):
        form = UserSignUpForm(data={
            'title': 'Herr',
            'first_name': 'Maximilian4',
            'last_name': 'Mustermann-Muster',
            'date_of_birth': '1990-1-1',
            'email': 'max@mustermann.com',
            'password1': 'Maximilian4',
            'password2': 'Maximilian4',
            'zip_code': '12345',
            'city': 'St.Ingbert',
            'street': 'Mecklenburgring',
            'house_number': '13',
            'phone': '152212345667',
            'username': 'MAXMU',
            'data_privacy': 'True'
        })
        self.assertFalse(form.is_valid())

    def test_signup_form_too_short_password(self):
        form = UserSignUpForm(data={
            'title': 'Herr',
            'first_name': 'Max',
            'last_name': 'Mustermann',
            'date_of_birth': '1990-1-1',
            'email': 'max@mustermann.com',
            'password1': 'HalloW4',
            'password2': 'HalloW4',
            'zip_code': '12345',
            'city': 'Musterstadt',
            'street': 'Mecklenburgring',
            'house_number': '13',
            'phone': '152212345667',
            'username': 'MAXMU',
            'data_privacy': 'True'
        })
        self.assertFalse(form.is_valid())

    def test_signup_form_password_just_numbers(self):
        form = UserSignUpForm(data={
            'title': 'Herr',
            'first_name': 'Max',
            'last_name': 'Mustermann',
            'date_of_birth': '1990-1-1',
            'email': 'max@mustermann.com',
            'password1': '123456789',
            'password2': '123456789',
            'zip_code': '12345',
            'city': 'Musterstadt',
            'street': 'Mecklenburgring',
            'house_number': '13',
            'phone': '152212345667',
            'username': 'MAXMU',
            'data_privacy': 'True'
        })
        self.assertFalse(form.is_valid())

    def test_signup_form_wrong_password_confirmation(self):
        form = UserSignUpForm(data={
            'title': 'Herr',
            'first_name': 'Max',
            'last_name': 'Mustermann',
            'date_of_birth': '1990-1-1',
            'email': 'max@mustermann.com',
            'password1': 'HalloWelt1',
            'password2': 'HalloWelt2',
            'zip_code': '12345',
            'city': 'Musterstadt',
            'street': 'Mecklenburgring',
            'house_number': '13',
            'phone': '152212345667',
            'username': 'MAXMU',
            'data_privacy': 'True'
        })
        self.assertFalse(form.is_valid())

    def test_signup_form_data_privacy_not_accepted(self):
        form = UserSignUpForm(data={
            'title': 'Herr',
            'first_name': 'Max',
            'last_name': 'Mustermann',
            'date_of_birth': '1990-1-1',
            'email': 'max@mustermann.com',
            'password1': 'HalloWelt1',
            'password2': 'HalloWelt1',
            'zip_code': '12345',
            'city': 'Musterstadt',
            'street': 'Mecklenburgring',
            'house_number': '13',
            'phone': '152212345667',
            'username': 'MAXMU',
            'data_privacy': 'False'
        })
        self.assertFalse(form.is_valid())

    def test_signup_form_empty(self):
        form = UserSignUpForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 15)

    def test_signup_form_nobel_name_1(self):
        form = UserSignUpForm(data={
            'title': 'Herr',
            'first_name': 'Max',
            'last_name': 'von Mustermann',
            'date_of_birth': '1990-1-1',
            'email': 'max@mustermann.com',
            'password1': 'kuchen123',
            'password2': 'kuchen123',
            'zip_code': '12345',
            'city': 'Musterstadt',
            'street': 'Mecklenburgring',
            'house_number': '13',
            'phone': '152212345667',
            'username': 'MAXMU',
            'data_privacy': 'True'
        })
        self.assertTrue(form.is_valid())

    def test_signup_form_nobel_name_2(self):
        form = UserSignUpForm(data={
            'title': 'Herr',
            'first_name': 'Max',
            'last_name': 'von dem Muster',
            'date_of_birth': '1990-1-1',
            'email': 'max@mustermann.com',
            'password1': 'kuchen123',
            'password2': 'kuchen123',
            'zip_code': '12345',
            'city': 'Musterstadt',
            'street': 'Mecklenburgring',
            'house_number': '13',
            'phone': '152212345667',
            'username': 'MAXMU',
            'data_privacy': 'True'
        })
        self.assertTrue(form.is_valid())

    def test_signup_form_special_phone(self):
        form = UserSignUpForm(data={
            'title': 'Herr',
            'first_name': 'Max',
            'last_name': 'von dem Muster',
            'date_of_birth': '1990-1-1',
            'email': 'max@mustermann.com',
            'password1': 'kuchen123',
            'password2': 'kuchen123',
            'zip_code': '12345',
            'city': 'Musterstadt',
            'street': 'Mecklenburgring',
            'house_number': '13',
            'phone': '+52212345667',
            'username': 'MAXMU',
            'data_privacy': 'True'
        })
        self.assertTrue(form.is_valid())

    def test_signup_form_special_phone_2(self):
        form = UserSignUpForm(data={
            'title': 'Herr',
            'first_name': 'Max',
            'last_name': 'von dem Muster',
            'date_of_birth': '1990-1-1',
            'email': 'max@mustermann.com',
            'password1': 'kuchen123',
            'password2': 'kuchen123',
            'zip_code': '12345',
            'city': 'Musterstadt',
            'street': 'Mecklenburgring',
            'house_number': '13',
            'phone': '0681/345667',
            'username': 'MAXMU',
            'data_privacy': 'True'
        })
        self.assertTrue(form.is_valid())
