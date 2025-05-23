from django.db import models

class Node(models.Model):
    id = models.CharField(max_length=100, primary_key=True, unique=True) 
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)   
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name    


