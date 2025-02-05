from django.db import models
from apps.base.models import BaseModel
from django.contrib.auth.models import User
# Create your models here.

class Chanel(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='chanel', blank=True, null=True)
    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='chanel/', blank=True, null=True)
    desc = models.TextField()
    banner = models.ImageField(upload_to='chanel_banners/', blank=True, null=True)
    followers = models.ManyToManyField(User, related_name='followed_channels', blank=True)

    class Meta:
        verbose_name = 'Chanel'
        verbose_name_plural = 'Chanels'

    def __str__(self):
        return self.name 

    
