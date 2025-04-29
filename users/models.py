from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Account(models.Model):
    ROLES = (
        ('ADMIN', 'System Administrator'),
        ('RANGER', 'Wildlife Ranger'),
        ('TECH', 'Technical Staff'),
        ('VIEWER', 'Read-Only Viewer')
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    role = models.CharField(max_length=10, choices=ROLES, default='VIEWER')
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    profile_pic = models.ImageField(upload_to='profiles/', null=True, blank=True)
    receive_alerts = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"
    

class UserSession(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    
    class Meta:
        verbose_name = "User Login Session"

# User.users = property(lambda u:Account.objects.get_or_create(user=u)[0])
# Lambda makes it possible to create user when they sign up