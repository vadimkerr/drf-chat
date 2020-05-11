from django.contrib.auth.models import User
from django.test import TestCase

from api.models import Message


class TestMessageModel(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(
            username="sender", password="sender_password"
        )

    def test_created(self):
        message = Message.objects.create(
            sender=self.sender, receiver=self.sender, text="hi there!"
        )
        self.assertEqual(message.pk, 1)
