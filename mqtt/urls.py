from django.urls import path
from .views import MqttDataView

urlpatterns = [
    path("mqtt-data/", MqttDataView.as_view(), name="mqtt-data"),
]