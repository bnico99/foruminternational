from django.test import TestCase
from info.models import InfoText, FAQEntry, FAQEntryEN, FAQEntryFR, PriceEntry, MailEntry


class TestModels(TestCase):

    def setUp(self):
        self.infotext1 = InfoText.objects.create(
            title='some_title',
            text='some_text'
        )
        self.faqentry1 = FAQEntry.objects.create(
            question_text='some_question',
            answer_text='some_answer'
        )

        self.faqentryen1 = FAQEntryEN.objects.create(
            question_text='some_question_en',
            answer_text='some_answer_en'
        )

        self.faqentryfr1 = FAQEntryFR.objects.create(
            question_text='some_question_fr',
            answer_text='some_answer_fr'
        )

        self.priceentry1 = PriceEntry.objects.create(
            title='price1',
            text = 100
        )

        self.mailentry1 = MailEntry.objects.create(
            title='some_mail',
            mail ='my_email'
        )

    def test_infotext_tostring(self):
        self.assertEqual(str(self.infotext1), 'some_title')

    def test_faqentry_tostring(self):
        self.assertEqual(str(self.faqentry1), "Question: " + 'some_question' + " - Answer: " + 'some_answer')

    def test_faqentryen_tostring(self):
        self.assertEqual(str(self.faqentryen1), "Question: " + 'some_question_en' + " - Answer: " + 'some_answer_en')

    def test_faqentryfr_tostring(self):
        self.assertEqual(str(self.faqentryfr1), "Question: " + 'some_question_fr' + " - Answer: " + 'some_answer_fr')

    def test_priceentry_tostring(self):
        self.assertEqual(str(self.priceentry1), 'price1')

    def test_mailentry_tostring(self):
        self.assertEqual(str(self.mailentry1), 'some_mail')
