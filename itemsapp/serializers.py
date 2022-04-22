from rest_framework import serializers


class ReceiptSerializer(serializers.Serializer):
    items = serializers.ListField()
