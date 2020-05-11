from rest_framework import serializers

from .models import Message


# Message serializer for read operations (get, list)
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


# Message serializer for write operations (post, put, patch)
class MessageWriteSerializer(serializers.ModelSerializer):
    # use request sender as message sender
    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Message
        fields = ["sender", "receiver", "text"]
