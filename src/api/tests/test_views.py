from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from api.models import Message


class BaseMessageTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="test_password")

        self.other_user = User.objects.create_user(
            username="other_user", password="test_password"
        )

        self.token = Token.objects.create(user=self.user)
        self.other_token = Token.objects.create(user=self.other_user)

        self.client = APIClient()
        self.other_client = APIClient()

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        self.other_client.credentials(HTTP_AUTHORIZATION=f"Token {self.other_token}")


class MessageCreateTestCase(BaseMessageTestCase):
    url = "/api/messages/"

    def test_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_message(self):
        response = self.client.post(
            self.url, {"receiver": self.other_user.pk, "text": "test message"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        message = Message.objects.get()
        self.assertEqual(message.sender, self.user)

    def test_neglect_sender(self):
        response = self.client.post(
            self.url,
            {
                "sender": self.other_user.pk,
                "receiver": self.other_user.pk,
                "text": "test message",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        message = Message.objects.get()
        self.assertEqual(message.sender, self.user)


class MessageListTestCase(BaseMessageTestCase):
    url = f"/api/messages/"

    def setUp(self):
        super().setUp()
        Message.objects.create(
            sender=self.user, receiver=self.other_user, text="first message"
        )
        Message.objects.create(
            sender=self.other_user, receiver=self.user, text="second message"
        )
        Message.objects.create(
            sender=self.other_user, receiver=self.other_user, text="third message"
        )

    def test_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_only_user_messages(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["text"], "first message")
        self.assertEqual(response.data[1]["text"], "second message")

        response = self.other_client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)


class MessageRetrieveTestCase(BaseMessageTestCase):
    def setUp(self):
        super().setUp()
        message = Message.objects.create(
            sender=self.user, receiver=self.user, text="test message"
        )
        self.url = f"/api/messages/{message.pk}/"

    def test_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retreive(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["text"], "test message")

    def test_retreive_not_sender_or_receiver(self):
        response = self.other_client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class MessageUpdateTestCase(BaseMessageTestCase):
    def setUp(self):
        super().setUp()
        message = Message.objects.create(
            sender=self.user, receiver=self.other_user, text="test message"
        )
        self.url = f"/api/messages/{message.pk}/"

    def test_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update(self):
        response = self.client.patch(self.url, {"text": "New message text"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        message = Message.objects.get()
        self.assertEqual(message.text, "New message text")

    def test_update_not_sender(self):
        response = self.other_client.patch(self.url, {"text": "New message text"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_sender_not_changed(self):
        response = self.client.patch(self.url, {"sender": self.other_user.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        message = Message.objects.get()
        self.assertEqual(message.sender, self.user)


class MessageDeleteTestCase(BaseMessageTestCase):
    def setUp(self):
        super().setUp()
        message = Message.objects.create(
            sender=self.user, receiver=self.other_user, text="test message"
        )
        self.url = f"/api/messages/{message.pk}/"

    def test_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertIs(Message.objects.all().exists(), False)

    def test_delete_not_sender(self):
        response = self.other_client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
