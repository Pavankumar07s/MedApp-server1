from rest_framework import serializers

class ChatResponseSerializer (serializers.Serializer):
    message = serializers.CharField()