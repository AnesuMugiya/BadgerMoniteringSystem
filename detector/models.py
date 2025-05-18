from django.db import models
from nodes.models import Node

class Detections(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    device = models.ForeignKey(Node, on_delete=models.CASCADE)
    detected = models.BooleanField()
    confidence = models.FloatField()
    image_path = models.CharField(max_length=255, default="static/images/latest.jpg")

    def __str__(self):
        return f"{self.timestamp} - {'BADGER' if self.detected else 'Clear'} ({self.confidence:.2f})"