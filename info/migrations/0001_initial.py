# Generated by Django 2.2.7 on 2020-01-22 10:21

from django.db import migrations, models

# Initially creates the Home Texts
def create_texts(apps, schema_editor):
    from info.models import InfoText

    for suffix in ['', 'EN', 'FR']:
        t = InfoText(title='Home' + suffix, text='Platzhalter Home' + suffix)
        t.save()

# Initially create PriceEntries
def create_prices(apps, schema_editor):
    from info.models import PriceEntry

    PriceEntry(title='Weekend noStudent 24h', text=240).save()
    PriceEntry(title='Weekend Student 24h', text=240).save()
    PriceEntry(title='Weekend noStudent 12h', text=125).save()
    PriceEntry(title='Weekend Student 12h', text=125).save()
    PriceEntry(title='Week under50 Student 3h', text=20).save()
    PriceEntry(title='Week over50 Student 3h', text=40).save()
    PriceEntry(title='Week under50 Student 6h', text=40).save()
    PriceEntry(title='Week over50 Student 6h', text=70).save()
    PriceEntry(title='Week under50 Student 12h', text=80).save()
    PriceEntry(title='Week over50 Student 12h', text=130).save()
    PriceEntry(title='Week under50 noStudent 3h', text=40).save()
    PriceEntry(title='Week over50 noStudent 3h', text=65).save()
    PriceEntry(title='Week under50 noStudent 6h', text=70).save()
    PriceEntry(title='Week over50 noStudent 6h', text=110).save()
    PriceEntry(title='Week under50 noStudent 12h', text=125).save()
    PriceEntry(title='Week over50 noStudent 12h', text=150).save()

    PriceEntry(title='Toilet Cleaning', text=40).save()

    PriceEntry(title='Cleaning noStudent', text=140).save()

    PriceEntry(title='Cleaning Student', text=40).save()

    PriceEntry(title='Deposit', text=200).save()

# Initially create MailEntries
def create_mail_addresses(apps, schema_editor):
    from info.models import MailEntry

    MailEntry(title='Cleaning', mail='forum.studentenwerk@example.com').save()
    MailEntry(title='Caretaker', mail='forum.studentenwerk@example.com').save()
    MailEntry(title='Tutor', mail='forum.studentenwerk@example.com').save()
    MailEntry(title='Admin', mail='forum.studentenwerk@example.com').save()

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FAQEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField(max_length=500, verbose_name='Question text')),
                ('answer_text', models.TextField(max_length=1000, verbose_name='Answer text')),
            ],
        ),
        migrations.CreateModel(
            name='FAQEntryEN',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField(max_length=500, verbose_name='Question text')),
                ('answer_text', models.TextField(max_length=1000, verbose_name='Answer text')),
            ],
        ),
        migrations.CreateModel(
            name='FAQEntryFR',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField(max_length=500, verbose_name='Question text')),
                ('answer_text', models.TextField(max_length=1000, verbose_name='Answer text')),
            ],
        ),
        migrations.CreateModel(
            name='InfoText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('text', models.TextField(verbose_name='Information text')),
            ],
        ),
        migrations.CreateModel(
            name='MailEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('mail', models.EmailField(max_length=254, verbose_name='Mail')),
            ],
        ),
        migrations.CreateModel(
            name='PriceEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('text', models.IntegerField(verbose_name='Price')),
            ],
        ),
        migrations.RunPython(create_texts),
        migrations.RunPython(create_prices),
        migrations.RunPython(create_mail_addresses),
    ]
