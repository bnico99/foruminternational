import time

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class TestFunctional(StaticLiveServerTestCase):
    serialized_rollback = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Firefox(executable_path='functional_tests/geckodriver')

    @classmethod
    def tearDownClass(cls):
        # cls.selenium.refresh()
        cls.selenium.quit()
        super().tearDownClass()

    def test_info_page_view_no_login(self):
        self.selenium.get(self.live_server_url + '/de')

        # get live url and add the url, which should be added(reverse dows not work on faq)
        test_url = self.live_server_url
        test_url = test_url + '/de/faq/'

        try:
            # if needed, open the Menu
            elem = self.selenium.find_element_by_xpath("//button [@data-toggle = 'collapse']")
            elem.click()
            # this sleep is essential, so the drop down menu can load
            time.sleep(1)
        except:
            pass
        # The User clicks on Information, to get to the faq Page
        # this sleep is essential, so the drop down menu can load
        elem = self.selenium.find_element_by_link_text("Informationen")
        elem.click()

        self.assertEqual(self.selenium.current_url, test_url)

    def test_registration_confirmation(self):
        self.selenium.get(self.live_server_url + '/de')

        try:
            # if needed, open the Menu
            elem = self.selenium.find_element_by_xpath("//button [@data-toggle = 'collapse']")
            elem.click()
            # this sleep is essential, so the drop down menu can load
            time.sleep(1)
        except:
            pass
        # The User clicks on Anmelden, to log in
        elem = self.selenium.find_element_by_link_text("Anmelden")
        elem.click()

        # User clicks on "Hier geht es zur Registrierung"
        elem = self.selenium.find_element_by_link_text("Hier geht es zur Registrierung")
        elem.click()

        # User enters his Information
        elem = self.selenium.find_element_by_id("id_username")
        elem.send_keys("test_user")

        elem = self.selenium.find_element_by_xpath("//input [@name ='email']")
        elem.send_keys("test_email@web.de")

        elem = self.selenium.find_element_by_id("id_password1")
        elem.send_keys("Passw0rt-")

        elem = self.selenium.find_element_by_id("id_password2")
        elem.send_keys("Passw0rt-")

        elem = self.selenium.find_element_by_id("id_first_name")
        elem.send_keys("Max")

        elem = self.selenium.find_element_by_id("id_last_name")
        elem.send_keys("Mustermann")

        elem = self.selenium.find_element_by_id("id_zip_code")
        elem.send_keys("12345")

        elem = self.selenium.find_element_by_id("id_city")
        elem.send_keys("Musterstadt")

        elem = self.selenium.find_element_by_id("id_street")
        elem.send_keys("Musterstraße")

        elem = self.selenium.find_element_by_id("id_house_number")
        elem.send_keys("42")

        elem = self.selenium.find_element_by_id("id_phone")
        elem.send_keys("123456789")

        elem = self.selenium.find_element_by_xpath("//input [@type = 'checkbox']")
        elem.click()

        # the user clicks on "Registrieren"
        elem = self.selenium.find_element_by_xpath("//button [@type = 'submit']")
        elem.click()

        # The right a tag must be shown (can't look at e-mails with this testing enviroment)
        elem = self.selenium.find_elements_by_xpath(
            "//*[contains(text(), 'Wir haben Ihnen eine E-Mail geschickt, bitte bestätigen Sie diese um Ihren Account zu aktivieren.')]")
        self.assertEqual(len(elem), 1)

    def test_login(self):
        # create a user, with which we can log in
        user1 = User.objects.create_user(username='Max',
                                         email='Max@example.com',
                                         password='Passw0rt1'
                                         )
        # creating a Profile is not needed for this test, user is enough

        self.selenium.get(self.live_server_url + '/de')

        try:
            # if needed, open the Menu
            elem = self.selenium.find_element_by_xpath("//button [@data-toggle = 'collapse']")
            elem.click()
            # this sleep is essential, so the drop down menu can load
            time.sleep(1)
        except:
            pass
        # The User clicks on Anmelden, to log in
        elem = self.selenium.find_element_by_link_text("Anmelden")
        elem.click()

        # enter login information of the user we added before
        elem = self.selenium.find_element_by_id("id_username")
        elem.send_keys("Max")

        elem = self.selenium.find_element_by_id("id_password")
        elem.send_keys("Passw0rt1")

        # click on the "Anmelden" button
        elem = self.selenium.find_element_by_xpath("//button [@type = 'submit']")
        elem.click()

        try:
            # if needed, open the Menu
            elem = self.selenium.find_element_by_xpath("//button [@data-toggle = 'collapse']")
            elem.click()
            # this sleep is essential, so the drop down menu can load
            time.sleep(1)
        except:
            pass

        # try to find the "Abmelden" button to confirm we are logged in
        # if it can't be found, then this test failed (assert something wrong)
        try:
            elem = self.selenium.find_element_by_link_text("Abmelden")
        except:
            self.assertEqual(0, 1)

    def test_show_calendar_when_logged_in(self):
        # create a user, with which we can log in
        user1 = User.objects.create_user(username='Max',
                                         email='Max@example.com',
                                         password='Passw0rt1'
                                         )
        # creating a Profile is not needed for this test, user is enough

        self.selenium.get(self.live_server_url + '/de')

        try:
            # if needed, open the Menu
            elem = self.selenium.find_element_by_xpath("//button [@data-toggle = 'collapse']")
            elem.click()
            # this sleep is essential, so the drop down menu can load
            time.sleep(1)
        except:
            pass
        # The User clicks on Anmelden, to log in
        elem = self.selenium.find_element_by_link_text("Anmelden")
        elem.click()

        # enter login information of the user we added before
        elem = self.selenium.find_element_by_id("id_username")
        elem.send_keys("Max")

        elem = self.selenium.find_element_by_id("id_password")
        elem.send_keys("Passw0rt1")

        # click on the "Anmelden" button
        elem = self.selenium.find_element_by_xpath("//button [@type = 'submit']")
        elem.click()

        try:
            # if needed, open the Menu
            elem = self.selenium.find_element_by_xpath("//button [@data-toggle = 'collapse']")
            elem.click()
            # this sleep is essential, so the drop down menu can load
            time.sleep(1)
        except:
            pass
            # The User clicks on Mieten, to go to the calendar
        elem = self.selenium.find_element_by_link_text("Mieten")
        elem.click()

        # try to find the calendar
        # if it can't be found, then this test failed (assert something wrong)
        try:
            elem = self.selenium.find_element_by_class_name("calendar")
        except:
            self.assertEqual(0, 1)

    def test_no_calendar_when_not_logged_in(self):
        self.selenium.get(self.live_server_url + '/de')

        try:
            # if needed, open the Menu
            elem = self.selenium.find_element_by_xpath("//button [@data-toggle = 'collapse']")
            elem.click()
            # this sleep is essential, so the drop down menu can load
            time.sleep(1)
        except:
            pass
        # The User clicks on Mieten, to go to the calendar
        elem = self.selenium.find_element_by_link_text("Mieten")
        elem.click()

        mistakes = True

        # try to find the calendar
        # if it can be found, don't change mistakes, so we throw an assertion error
        try:
            elem = self.selenium.find_element_by_class_name("calendar")
        except:
            mistakes = False

        if (mistakes):
            self.assertEqual(0, 1)

    def test_change_to_english(self):
        self.selenium.get(self.live_server_url + '/de')

        # get server_url and add eng for testing later
        test_url = self.live_server_url
        test_url = test_url + '/en/'

        try:
            # if needed, open the Menu
            elem = self.selenium.find_element_by_xpath("//button [@data-toggle = 'collapse']")
            elem.click()
            # this sleep is essential, so the drop down menu can load
            time.sleep(1)
        except:
            pass
            # The User tries to change language
        # look for the change language button and click it
        elem = self.selenium.find_element_by_id("navbarDropdown")
        elem.click()

        # change Language to English
        elem = self.selenium.find_element_by_link_text("English")
        elem.click()

        self.assertEqual(self.selenium.current_url, test_url)

    def test_change_to_french(self):
        self.selenium.get(self.live_server_url + '/de')

        # get server_url and add eng for testing later
        test_url = self.live_server_url
        test_url = test_url + '/fr/'

        try:
            # if needed, open the Menu
            elem = self.selenium.find_element_by_xpath("//button [@data-toggle = 'collapse']")
            elem.click()
            # this sleep is essential, so the drop down menu can load
            time.sleep(1)
        except:
            pass
        # The User tries to change language
        # look for the change language button and click it
        elem = self.selenium.find_element_by_id("navbarDropdown")
        elem.click()

        # Change language to french
        elem = self.selenium.find_element_by_link_text("Français")
        elem.click()

        self.assertEqual(self.selenium.current_url, test_url)

    def test_change_to_eng_and_back(self):
        self.selenium.get(self.live_server_url + '/de')

        # get server_url and add eng for testing later
        test_url = self.live_server_url
        test_url = test_url + '/de/'

        try:
            # if needed, open the Menu
            elem = self.selenium.find_element_by_xpath("//button [@data-toggle = 'collapse']")
            elem.click()
            # this sleep is essential, so the drop down menu can load
            time.sleep(1)
        except:
            pass
        # The User tries to change language
        # look for the change language button and click it
        elem = self.selenium.find_element_by_id("navbarDropdown")
        elem.click()

        # change language to english
        elem = self.selenium.find_element_by_link_text("English")
        elem.click()

        try:
            # if needed, open the Menu
            elem = self.selenium.find_element_by_xpath("//button [@data-toggle = 'collapse']")
            elem.click()
            # this sleep is essential, so the drop down menu can load
            time.sleep(1)
        except:
            pass
        # The User tries to change language
        # look for the change language button and click it
        elem = self.selenium.find_element_by_id("navbarDropdown")
        elem.click()

        # change language to english
        elem = self.selenium.find_element_by_link_text("Deutsch")
        elem.click()

        self.assertEqual(self.selenium.current_url, test_url)

    def test_go_to_Mein_Account(self):
        # create a user, with which we can log in
        user1 = User.objects.create_user(username='Max',
                                         email='Max@example.com',
                                         password='Passw0rt1'
                                         )
        # creating a Profile is not needed for this test, user is enough

        self.selenium.get(self.live_server_url + '/de')

        # get server_url and add /de/register/myaccount_edit
        test_url = self.live_server_url
        test_url = test_url + '/de/register/myaccount_edit'

        try:
            # if needed, open the Menu
            elem = self.selenium.find_element_by_xpath("//button [@data-toggle = 'collapse']")
            elem.click()
            # this sleep is essential, so the drop down menu can load
            time.sleep(1)
        except:
            pass
        # The User clicks on Anmelden, to log in
        elem = self.selenium.find_element_by_link_text("Anmelden")
        elem.click()

        # enter login information of the user we added before
        elem = self.selenium.find_element_by_id("id_username")
        elem.send_keys("Max")

        elem = self.selenium.find_element_by_id("id_password")
        elem.send_keys("Passw0rt1")

        # click on the "Anmelden" button
        elem = self.selenium.find_element_by_xpath("//button [@type = 'submit']")
        elem.click()

        try:
            # if needed, open the Menu
            elem = self.selenium.find_element_by_xpath("//button [@data-toggle = 'collapse']")
            elem.click()
            # this sleep is essential, so the drop down menu can load
            time.sleep(1)
        except:
            pass
        # The User clicks on Anmelden, to log in
        elem = self.selenium.find_element_by_link_text("Mein Account")
        elem.click()

        self.assertEqual(self.selenium.current_url, test_url)

    def test_go_next_month_calendar_ger(self):
        # create a user, with which we can log in
        user1 = User.objects.create_user(username='Max',
                                         email='Max@example.com',
                                         password='Passw0rt1'
                                         )
        # creating a Profile is not needed for this test, user is enough

        self.selenium.get(self.live_server_url + '/de')
        try:
            # if needed, open the Menu
            elem = self.selenium.find_element_by_xpath("//button [@data-toggle = 'collapse']")
            elem.click()
            # this sleep is essential, so the drop down menu can load
            time.sleep(1)
        except:
            pass
        # The User clicks on Anmelden, to log in
        # look for the change language button and click it
        elem = self.selenium.find_element_by_id("navbarDropdown")
        elem.click()

        # change Language to English
        elem = self.selenium.find_element_by_link_text("Deutsch")
        elem.click()

        try:
            # if needed, open the Menu
            elem = self.selenium.find_element_by_xpath("//button [@data-toggle = 'collapse']")
            elem.click()
            # this sleep is essential, so the drop down menu can load
            time.sleep(1)
        except:
            pass
        # The User clicks on Anmelden, to log in
        # Go to "Anmelden"
        elem = self.selenium.find_element_by_link_text("Anmelden")
        elem.click()

        # enter login information of the user we added before
        elem = self.selenium.find_element_by_id("id_username")
        elem.send_keys("Max")

        elem = self.selenium.find_element_by_id("id_password")
        elem.send_keys("Passw0rt1")

        # click on the "Anmelden" button
        elem = self.selenium.find_element_by_xpath("//button [@type = 'submit']")
        elem.click()

        try:
            # if needed, open the Menu
            elem = self.selenium.find_element_by_xpath("//button [@data-toggle = 'collapse']")
            elem.click()
            # this sleep is essential, so the drop down menu can load
            time.sleep(1)
        except:
            pass
        # The User clicks on Anmelden, to log in
        elem = self.selenium.find_element_by_link_text("Mieten")
        elem.click()

        # try to find Buttons to switch to the next month
        # if not found, then we have an error
        try:
            elem = self.selenium.find_element_by_xpath("//a [@class = 'btn btn-secondary float-right']")
            elem.click()
        except:
            self.assertEqual(0, 1)

        # try to find Buttons to switch to the prev and next month
        # if not found, then we have an error
        try:
            elem = self.selenium.find_element_by_xpath("//a [@class = 'btn btn-secondary float-left']")
        except:
            self.assertEqual(0, 1)

        try:
            elem = self.selenium.find_element_by_xpath("//a [@class = 'btn btn-secondary float-right']")
        except:
            self.assertEqual(0, 1)

    def test_go_next_month_calendar_eng(self):
        # create a user, with which we can log in
        user1 = User.objects.create_user(username='Max',
                                         email='Max@example.com',
                                         password='Passw0rt1'
                                         )
        # creating a Profile is not needed for this test, user is enough

        self.selenium.get(self.live_server_url + '/de')

        try:
            # if needed, open the Menu
            elem = self.selenium.find_element_by_xpath("//button [@data-toggle = 'collapse']")
            elem.click()
            # this sleep is essential, so the drop down menu can load
            time.sleep(1)
        except:
            pass
        # The User clicks on Anmelden, to log in
        # look for the change language button and click it
        elem = self.selenium.find_element_by_id("navbarDropdown")
        elem.click()
        # change Language to English
        elem = self.selenium.find_element_by_link_text("English")
        elem.click()

        try:
            # if needed, open the Menu
            elem = self.selenium.find_element_by_xpath("//button [@data-toggle = 'collapse']")
            elem.click()
            # this sleep is essential, so the drop down menu can load
            time.sleep(1)
        except:
            pass
        # The User clicks on Anmelden, to log in
        # Go to "Anmelden"
        elem = self.selenium.find_element_by_link_text("Login")
        elem.click()

        # enter login information of the user we added before
        elem = self.selenium.find_element_by_id("id_username")
        elem.send_keys("Max")

        elem = self.selenium.find_element_by_id("id_password")
        elem.send_keys("Passw0rt1")

        # click on the "Anmelden" button
        elem = self.selenium.find_element_by_xpath("//button [@type = 'submit']")
        elem.click()

        try:
            # if needed, open the Menu
            elem = self.selenium.find_element_by_xpath("//button [@data-toggle = 'collapse']")
            elem.click()
            # this sleep is essential, so the drop down menu can load
            time.sleep(1)
        except:
            pass
        # The User clicks on Anmelden, to log in
        elem = self.selenium.find_element_by_link_text("Book")
        elem.click()

        # try to find Buttons to switch to next month
        # if not found, then we have an error
        try:
            elem = self.selenium.find_element_by_xpath("//a [@class = 'btn btn-secondary float-right']")
            elem.click()
        except:
            self.assertEqual(0, 1)

        # try to find Buttons to switch to prev and next month
        # if not found, then we have an error
        try:
            elem = self.selenium.find_element_by_xpath("//a [@class = 'btn btn-secondary float-left']")
        except:
            self.assertEqual(0, 1)

        try:
            elem = self.selenium.find_element_by_xpath("//a [@class = 'btn btn-secondary float-right']")
        except:
            self.assertEqual(0, 1)

    def test_double_registration(self):
        self.selenium.get(self.live_server_url + '/de')

        try:
            # if needed, open the Menu
            elem = self.selenium.find_element_by_xpath("//button [@data-toggle = 'collapse']")
            elem.click()
            # this sleep is essential, so the drop down menu can load
            time.sleep(1)
        except:
            pass
        # The User clicks on Anmelden, to log in
        # click on "Anmelden"
        elem = self.selenium.find_element_by_link_text("Anmelden")
        elem.click()

        # User clicks on "Hier geht es zur Registrierung"
        elem = self.selenium.find_element_by_link_text("Hier geht es zur Registrierung")
        elem.click()

        # User enters his Information
        elem = self.selenium.find_element_by_id("id_username")
        elem.send_keys("test_user")

        elem = self.selenium.find_element_by_id("id_email")
        elem.send_keys("test_email@web.de")

        elem = self.selenium.find_element_by_id("id_password1")
        elem.send_keys("Passw0rt-")

        elem = self.selenium.find_element_by_id("id_password2")
        elem.send_keys("Passw0rt-")

        elem = self.selenium.find_element_by_id("id_first_name")
        elem.send_keys("Max")

        elem = self.selenium.find_element_by_id("id_last_name")
        elem.send_keys("Mustermann")

        elem = self.selenium.find_element_by_id("id_zip_code")
        elem.send_keys("12345")

        elem = self.selenium.find_element_by_id("id_city")
        elem.send_keys("Musterstadt")

        elem = self.selenium.find_element_by_id("id_street")
        elem.send_keys("Musterstraße")

        elem = self.selenium.find_element_by_id("id_house_number")
        elem.send_keys("42")

        elem = self.selenium.find_element_by_id("id_phone")
        elem.send_keys("123456789")

        elem = self.selenium.find_element_by_xpath("//input [@type = 'checkbox']")
        elem.click()

        # the user clicks on "Registrieren"
        elem = self.selenium.find_element_by_xpath("//button [@type = 'submit']")
        elem.click()

        elem = self.selenium.find_element_by_tag_name('a')
        elem.click()

        # try to create a user with the same username

        # The User clicks on Anmelden, to log in
        # click on "Anmelden"
        elem = self.selenium.find_element_by_link_text("Anmelden")
        elem.click()

        # User clicks on "Hier geht es zur Registrierung"
        elem = self.selenium.find_element_by_link_text("Hier geht es zur Registrierung")
        elem.click()

        # User enters his Information
        elem = self.selenium.find_element_by_id("id_username")
        elem.send_keys("test_user")

        elem = self.selenium.find_element_by_id("id_email")
        elem.send_keys("test_email2@web.de")

        elem = self.selenium.find_element_by_id("id_password1")
        elem.send_keys("Passw0rt-")

        elem = self.selenium.find_element_by_id("id_password2")
        elem.send_keys("Passw0rt-")

        elem = self.selenium.find_element_by_id("id_first_name")
        elem.send_keys("Moritz")

        elem = self.selenium.find_element_by_id("id_last_name")
        elem.send_keys("Chaosmann")

        elem = self.selenium.find_element_by_id("id_zip_code")
        elem.send_keys("54321")

        elem = self.selenium.find_element_by_id("id_city")
        elem.send_keys("Chaosstadt")

        elem = self.selenium.find_element_by_id("id_street")
        elem.send_keys("Chaosstraße")

        elem = self.selenium.find_element_by_id("id_house_number")
        elem.send_keys("69")

        elem = self.selenium.find_element_by_id("id_phone")
        elem.send_keys("987654321")
        elem = self.selenium.find_element_by_xpath("//input [@type = 'checkbox']")
        elem.click()

        # the user clicks on "Registrieren"
        elem = self.selenium.find_element_by_xpath("//button [@type = 'submit']")
        elem.click()

        # try to find the fail text
        # if it can't be found, something wrong happened(for example second account with same name got accepted)
        try:
            elem = self.selenium.find_element_by_xpath("//p [@style = 'color: red']")
        except:
            self.assertEqual(0, 1)

    def test_change_account_name(self):
        # create a user, with which we can log in
        user1 = User.objects.create_user(username='Max',
                                         email='Max@example.com',
                                         password='Passw0rt1'
                                         )
        # creating a Profile is not needed for this test, user is enough
        self.selenium.get(self.live_server_url + '/de')

        try:
            # if needed, open the Menu
            elem = self.selenium.find_element_by_xpath("//button [@data-toggle = 'collapse']")
            elem.click()
            # this sleep is essential, so the drop down menu can load
            time.sleep(1)
        except:
            pass
        # The User clicks on Anmelden, to log in
        # Go to "Anmelden"
        elem = self.selenium.find_element_by_link_text("Anmelden")
        elem.click()

        # enter login information of the user we added before
        elem = self.selenium.find_element_by_id("id_username")
        elem.send_keys("Max")

        elem = self.selenium.find_element_by_id("id_password")
        elem.send_keys("Passw0rt1")

        # click on the "Anmelden" button
        elem = self.selenium.find_element_by_xpath("//button [@type = 'submit']")
        elem.click()

        try:
            # if needed, open the Menu
            elem = self.selenium.find_element_by_xpath("//button [@data-toggle = 'collapse']")
            elem.click()
            # this sleep is essential, so the drop down menu can load
            time.sleep(1)
        except:
            pass
        # The User clicks on Anmelden, to log in
        # go to "Mein Account"
        elem = self.selenium.find_element_by_link_text("Mein Account")
        elem.click()

        # click "Bearbeiten" for the name etc.
        elem = self.selenium.find_element_by_xpath("//a [@href = 'myaccount_edit?edit=1#name']")
        elem.click()

        # enter new first name
        elem = self.selenium.find_element_by_xpath("//input [@name = 'first_name']")
        elem.send_keys("Max_firstname")

        # enter new last name
        elem = self.selenium.find_element_by_xpath("//input [@name = 'last_name']")
        elem.send_keys("Mustermann_lastname")

        # enter new day of birth
        elem = self.selenium.find_element_by_xpath("//select [@name = 'date_of_birth_day']")
        elem.send_keys("1")

        # enter new month of birth
        elem = self.selenium.find_element_by_xpath("//select [@name = 'date_of_birth_month']")
        elem.send_keys("Mai")

        # enter new year of birth
        elem = self.selenium.find_element_by_xpath("//select [@name = 'date_of_birth_year']")
        elem.send_keys("1970")

        # click "speichern"
        elem = self.selenium.find_element_by_xpath("//button [@name = 'speichern']")
        elem.click()

        # try to find the Confirmation. If it can't be found, there was an error
        try:
            elem = self.selenium.find_element_by_xpath("//h1 [@style ='text-align:center;']")
        except:
            self.assertEqual(0, 1)

    def test_change_account_address(self):
        # create a user, with which we can log in
        user1 = User.objects.create_user(username='Max',
                                         email='Max@example.com',
                                         password='Passw0rt1'
                                         )
        # creating a Profile is not needed for this test, user is enough
        self.selenium.get(self.live_server_url + '/de')

        try:
            # if needed, open the Menu
            elem = self.selenium.find_element_by_xpath("//button [@data-toggle = 'collapse']")
            elem.click()
            # this sleep is essential, so the drop down menu can load
            time.sleep(1)
        except:
            pass
        # The User clicks on Anmelden, to log in
        # Go to "Anmelden"
        elem = self.selenium.find_element_by_link_text("Anmelden")
        elem.click()

        # enter login information of the user we added before
        elem = self.selenium.find_element_by_id("id_username")
        elem.send_keys("Max")

        elem = self.selenium.find_element_by_id("id_password")
        elem.send_keys("Passw0rt1")

        # click on the "Anmelden" button
        elem = self.selenium.find_element_by_xpath("//button [@type = 'submit']")
        elem.click()

        try:
            # if needed, open the Menu
            elem = self.selenium.find_element_by_xpath("//button [@data-toggle = 'collapse']")
            elem.click()
            # this sleep is essential, so the drop down menu can load
            time.sleep(1)
        except:
            pass
        # The User clicks on Anmelden, to log in
        # go to "Mein Account"
        elem = self.selenium.find_element_by_link_text("Mein Account")
        elem.click()

        # click "Bearbeiten" for the Adress 
        elem = self.selenium.find_element_by_xpath("//a [@href = 'myaccount_edit?edit=2#adress']")
        elem.click()

        # enter new zip_code, delete "NONE" first
        elem = self.selenium.find_element_by_xpath("//input [@name = 'zip_code']")
        elem.send_keys(Keys.BACKSPACE)
        elem.send_keys(Keys.BACKSPACE)
        elem.send_keys(Keys.BACKSPACE)
        elem.send_keys(Keys.BACKSPACE)
        elem.send_keys("12345")

        # add a city name
        elem = self.selenium.find_element_by_xpath("//input [@name = 'city']")
        elem.send_keys("Musterstadt")

        # add a street name
        elem = self.selenium.find_element_by_xpath("//input [@name = 'street']")
        elem.send_keys("Musterstraße")

        # add a house number, delete "NONE" first
        elem = self.selenium.find_element_by_xpath("//input [@name = 'house_number']")
        elem.send_keys(Keys.BACKSPACE)
        elem.send_keys(Keys.BACKSPACE)
        elem.send_keys(Keys.BACKSPACE)
        elem.send_keys(Keys.BACKSPACE)
        elem.send_keys("42")

        # click "speichern"
        elem = self.selenium.find_element_by_xpath("//button [@name = 'speichern']")
        elem.click()

        # try to find the Confirmation. If it can't be found, there was an error
        try:
            elem = self.selenium.find_element_by_xpath("//h1 [@style ='text-align:center;']")
        except:
            self.assertEqual(0, 1)

    def test_change_account_email_and_phone(self):
        # create a user, with which we can log in
        user1 = User.objects.create_user(username='Max',
                                         email='Max@example.com',
                                         password='Passw0rt1'
                                         )
        # creating a Profile is not needed for this test, user is enough
        self.selenium.get(self.live_server_url + '/de')

        try:
            # if needed, open the Menu
            elem = self.selenium.find_element_by_xpath("//button [@data-toggle = 'collapse']")
            elem.click()
            # this sleep is essential, so the drop down menu can load
            time.sleep(1)
        except:
            pass
        # The User clicks on Anmelden, to log in
        # Go to "Anmelden"
        elem = self.selenium.find_element_by_link_text("Anmelden")
        elem.click()

        # enter login information of the user we added before
        elem = self.selenium.find_element_by_id("id_username")
        elem.send_keys("Max")

        elem = self.selenium.find_element_by_id("id_password")
        elem.send_keys("Passw0rt1")

        # click on the "Anmelden" button
        elem = self.selenium.find_element_by_xpath("//button [@type = 'submit']")
        elem.click()

        try:
            # if needed, open the Menu
            elem = self.selenium.find_element_by_xpath("//button [@data-toggle = 'collapse']")
            elem.click()
            # this sleep is essential, so the drop down menu can load
            time.sleep(1)
        except:
            pass
        # The User clicks on Anmelden, to log in
        # go to "Mein Account"
        elem = self.selenium.find_element_by_link_text("Mein Account")
        elem.click()

        # click "Bearbeiten" for the email and phone number
        elem = self.selenium.find_element_by_xpath("//a [@href = 'myaccount_edit?edit=3#number']")
        elem.click()

        # add a now phonenumber, delete "NONE" first
        elem = self.selenium.find_element_by_xpath("//input [@name = 'phone']")

        elem.send_keys(Keys.BACKSPACE)
        elem.send_keys(Keys.BACKSPACE)
        elem.send_keys(Keys.BACKSPACE)
        elem.send_keys(Keys.BACKSPACE)

        elem.send_keys("987654321")

        # click "speichern"
        elem = self.selenium.find_element_by_xpath("//button [@name = 'speichern']")
        elem.click()

        # try to find the Confirmation. If it can't be found, there was an error
        try:
            elem = self.selenium.find_element_by_xpath("//h1 [@style ='text-align:center;']")
        except:
            self.assertEqual(0, 1)

    def test_change_account_password(self):
        # create a user, with which we can log in
        user1 = User.objects.create_user(username='Max',
                                         email='Max@example.com',
                                         password='Passw0rt1'
                                         )
        # creating a Profile is not needed for this test, user is enough
        self.selenium.get(self.live_server_url + '/de')

        try:
            # if needed, open the Menu
            elem = self.selenium.find_element_by_xpath("//button [@data-toggle = 'collapse']")
            elem.click()
            # this sleep is essential, so the drop down menu can load
            time.sleep(1)
        except:
            pass
        # The User clicks on Anmelden, to log in
        # Go to "Anmelden"
        elem = self.selenium.find_element_by_link_text("Anmelden")
        elem.click()

        # enter login information of the user we added before
        elem = self.selenium.find_element_by_id("id_username")
        elem.send_keys("Max")

        elem = self.selenium.find_element_by_id("id_password")
        elem.send_keys("Passw0rt1")

        # click on the "Anmelden" button
        elem = self.selenium.find_element_by_xpath("//button [@type = 'submit']")
        elem.click()

        try:
            # if needed, open the Menu
            elem = self.selenium.find_element_by_xpath("//button [@data-toggle = 'collapse']")
            elem.click()
            # this sleep is essential, so the drop down menu can load
            time.sleep(1)
        except:
            pass
        # go to "Mein Account"
        elem = self.selenium.find_element_by_link_text("Mein Account")
        elem.click()

        # click "Bearbeiten" for the password
        elem = self.selenium.find_element_by_xpath("//a [@href = 'myaccount_edit?edit=5#pw']")
        elem.click()

        # enter first password
        elem = self.selenium.find_element_by_xpath("//input [@name = 'password']")
        elem.send_keys("new_password1")

        # enter confirmation password
        elem = self.selenium.find_element_by_xpath("//input [@name = 'passwordconfirm']")
        elem.send_keys("new_password1")

        # click "speichern"
        elem = self.selenium.find_element_by_xpath("//button [@name = 'speichern']")
        elem.click()

        # can't check password in the way we checked the other inputs, so log out and try to log in with new password
        try:
            # if needed, open the Menu
            elem = self.selenium.find_element_by_xpath("//button [@data-toggle = 'collapse']")
            elem.click()
            # this sleep is essential, so the drop down menu can load
            time.sleep(1)
        except:
            pass
        # The User clicks on Abmelden, to log out
        elem = self.selenium.find_element_by_link_text("Abmelden")
        elem.click()

        try:
            # if needed, open the Menu
            elem = self.selenium.find_element_by_xpath("//button [@data-toggle = 'collapse']")
            elem.click()
            # this sleep is essential, so the drop down menu can load
            time.sleep(1)
        except:
            pass
        # The User clicks on Anmelden, to log in
        # Go to "Anmelden"
        elem = self.selenium.find_element_by_link_text("Anmelden")
        elem.click()

        # enter login information of the user we added before
        elem = self.selenium.find_element_by_id("id_username")
        elem.send_keys("Max")

        elem = self.selenium.find_element_by_id("id_password")
        elem.send_keys("new_password1")

        # click on the "Anmelden" button
        elem = self.selenium.find_element_by_xpath("//button [@type = 'submit']")
        elem.click()

        try:
            # try to to go to "Mein Account"
            # if we can't then we have an error
            try:
                # if needed, open the Menu
                elem = self.selenium.find_element_by_xpath("//button [@data-toggle = 'collapse']")
                elem.click()
                # this sleep is essential, so the drop down menu can load
                time.sleep(1)
            except:
                pass
            elem = self.selenium.find_element_by_link_text("Mein Account")
            elem.click()
        except:
            self.assertEqual(0, 1)
