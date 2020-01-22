from django.test import TestCase
from booking.forms import BookingForm

import datetime

class TestForms(TestCase):

    def test_valid(self):
        form = BookingForm(data={
            'date': datetime.date(2020, 5, 9),
            'start_time': datetime.time(hour=8, minute=0),
            'duration': 12,
            'student': 'yes',
            'number_people': 5,
            'refrigerator': 'yes',
            'occasion': 'party'})

        self.assertTrue(form.is_valid(), form.errors)

    # should not be possible because it is not selectable
    def test_invalid_start(self):
        form = BookingForm(data={
            'date': datetime.date(2020, 5, 9),
            'start_time': datetime.time(hour=0, minute=1),
            'duration': 12,
            'student': 'yes',
            'number_people': 5,
            'refrigerator': 'yes',
            'occasion': 'party'})
        self.assertFalse(form.is_valid(), form.errors)

    # should not be possible because it is not selectable
    def test_invalid_start2(self):
        form = BookingForm(data={
            'date': datetime.date(2020, 5, 9),
            'start_time': '11:30',
            'duration': 12,
            'student': 'yes',
            'number_people': 5,
            'refrigerator': 'yes',
            'occasion': 'party'})
        self.assertFalse(form.is_valid(), form.errors)

    # should not be possible because it is not selectable
    def test_invalid_duration(self):
        form = BookingForm(data={
            'date': datetime.date(2020, 5, 8),
            'start_time': '16:00',
            'duration': 5,
            'student': 'yes',
            'number_people': 5,
            'refrigerator': 'yes',
            'occasion': 'party'})
        self.assertFalse(form.is_valid(), form.errors)

    def test_valid_nostudent(self):
        form = BookingForm(data={
            'date': datetime.date(2020, 5, 8),
            'start_time': '16:00',
            'duration': 6,
            'student': 'no',
            'number_people': 5,
            'refrigerator': 'yes',
            'occasion': 'party'})
        self.assertTrue(form.is_valid(), form.errors)

    def test_valid_manypeople(self):
        form = BookingForm(data={
            'date': datetime.date(2020, 5, 8),
            'start_time': '16:00',
            'duration': 6,
            'student': 'no',
            'number_people': 500,
            'refrigerator': 'yes',
            'occasion': 'party'})
        self.assertTrue(form.is_valid(), form.errors)

    def test_invalid_zeropeople(self):
        form = BookingForm(data={
            'date': datetime.date(2020, 5, 9),
            'start_time': '11:00',
            'duration': 12,
            'student': 'no',
            'number_people': 0,
            'refrigerator': 'yes',
            'occasion': 'party'})
        self.assertFalse(form.is_valid(), form.errors)

    def test_invalid_minuspeople(self):
        form = BookingForm(data={
            'date': datetime.date(2020, 5, 9),
            'start_time': '11:00',
            'duration': 12,
            'student': 'no',
            'number_people': -6,
            'refrigerator': 'yes',
            'occasion': 'party'})
        self.assertFalse(form.is_valid(), form.errors)

    def test_valid_occasion(self):
        form = BookingForm(data={
            'date': datetime.date(2020, 5, 9),
            'start_time': '11:00',
            'duration': 12,
            'student': 'no',
            'number_people': 10,
            'refrigerator': 'yes',
            'occasion': '123'})
        self.assertTrue(form.is_valid(), form.errors)

    def test_invalid_nooccasion(self):
        form = BookingForm(data={
            'date': datetime.date(2020, 5, 9),
            'start_time': '11:00',
            'duration': 12,
            'student': 'no',
            'number_people': 10,
            'refrigerator': 'yes',
            'occasion': ''})
        self.assertFalse(form.is_valid(), form.errors)
