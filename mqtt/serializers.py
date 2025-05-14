from rest_framework import serializers

class MqttMessageSerializer(serializers.Serializer):
    message = serializers.JSONField()