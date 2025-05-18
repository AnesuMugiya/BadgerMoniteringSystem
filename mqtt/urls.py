from django.urls import path
from .views import MqttDataView, aiprocessing


urlpatterns = [
    path("mqtt-data/", MqttDataView.as_view(), name="mqtt-data"),
    path("aip/", aiprocessing, name="aiprocessing"),
]