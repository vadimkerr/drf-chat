from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.test import TestCase

from api.models import Message


class TestMessageModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="user_password")

    def test_created(self):
        message = Message.objects.create(
            sender=self.user, receiver=self.user, text="hi there!"
        )
        self.assertEqual(message.pk, 1)

    def test_create_with_empty_text(self):
        with self.assertRaises(IntegrityError) as context:
            Message.objects.create(sender=self.user, receiver=self.user, text="")
