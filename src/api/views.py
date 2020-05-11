from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated

from .models import Message
from .permissions import IsReceiver, IsSender
from .serializers import MessageSerializer, MessageWriteSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated & (IsSender | IsReceiver)]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(Q(sender=user) | Q(receiver=user))

    def get_serializer_class(self):
        if self.request.method not in SAFE_METHODS:
            return MessageWriteSerializer

        return MessageSerializer
