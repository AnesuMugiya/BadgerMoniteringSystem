from django.db import models
from nodes.models import Node

def output_path(instance, filename):
    return "detector/node_{0}/{1}".format(instance.node.name, filename)

class ImageFiles(models.Model):
    image = models.ImageField(upload_to='images/')
    timestamp = models.DateTimeField(auto_now_add=True)
    node = models.ForeignKey(Node, on_delete=models.CASCADE)

    def __str__(self):
        return f"Image {self.id} - {self.timestamp}"

class Detections(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    detected = models.BooleanField()
    confidence = models.FloatField()
    input = models.OneToOneField(ImageFiles, on_delete=models.CASCADE)
    output = models.ImageField(upload_to=output_path)

    def __str__(self):
        return f"{self.timestamp} - {'BADGER' if self.detected else 'Clear'} ({self.confidence:.2f})"
    