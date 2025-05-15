from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache
from .serializers import MqttMessageSerializer

class MqttDataView(APIView):
    def get(self, request):
        data = cache.get("mqtt_data", {}) # Retrieve data from cache
        serializer = MqttMessageSerializer(data={"message": data})
        if serializer.is_valid():
            return Response(serializer.data) # Return the cached data
        return Response(serializer.errors, status=400)