from django.db import models
from nodes.models import Node

def output_path(instance, filename):
    return "detector/node_{0}/{1}".format(instance.input.node.name, filename)

class ImageFile(models.Model):
    image = models.ImageField(upload_to='images/')
    timestamp = models.DateTimeField(auto_now_add=True)
    node = models.ForeignKey(Node, on_delete=models.CASCADE)

    def __str__(self):
        return f"Image {self.id} - {self.timestamp}"

class Detection(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    detected = models.BooleanField()
    confidence = models.FloatField()
    input = models.OneToOneField(ImageFile, on_delete=models.CASCADE)
    output = models.ImageField(upload_to=output_path)

    def __str__(self):
        return f"{self.timestamp} - {self.detected} - {'BADGER' if self.detected else 'Clear'} ({self.confidence:.2f})"
