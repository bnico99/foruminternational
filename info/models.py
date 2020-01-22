from django.db import models


class InfoText(models.Model):
    """Database entry for text on Home page consisting of identifying title and the text"""
    title = models.CharField('Title', max_length=100)
    text = models.TextField('Information text')

    def __str__(self):
        return self.title


class FAQEntry(models.Model):
    """Database entry for a German FAQ entries consisting of question and answer"""
    question_text = models.TextField('Question text', max_length=500)
    answer_text = models.TextField('Answer text', max_length=1000)

    def __str__(self):
        return "Question: " + self.question_text + " - Answer: " + self.answer_text


class FAQEntryEN(models.Model):
    """Database entry for an English FAQ entries consisting of question and answer"""
    question_text = models.TextField('Question text', max_length=500)
    answer_text = models.TextField('Answer text', max_length=1000)

    def __str__(self):
        return "Question: " + self.question_text + " - Answer: " + self.answer_text


class FAQEntryFR(models.Model):
    """Database entry for a French FAQ entries consisting of question and answer"""
    question_text = models.TextField('Question text', max_length=500)
    answer_text = models.TextField('Answer text', max_length=1000)

    def __str__(self):
        return "Question: " + self.question_text + " - Answer: " + self.answer_text


class PriceEntry(models.Model):
    """Database entry for a price entries consisting of an identifying title and the price"""
    title = models.CharField('Title', max_length=100)
    text = models.IntegerField('Price')

    def __str__(self):
        return self.title


class MailEntry(models.Model):
    """Database entry for a mail address entry consisting of an identify title and the mail address"""
    title = models.CharField('Title', max_length=100)
    mail = models.EmailField('Mail', max_length=254)

    def __str__(self):
        return self.title
