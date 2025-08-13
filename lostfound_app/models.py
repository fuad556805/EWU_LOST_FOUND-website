from django.db import models
from django.contrib.auth.models import User

class FoundItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    date_reported = models.DateField(auto_now_add=True)
    contact_info = models.CharField(max_length=150, blank=True)

class LostItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    date_reported = models.DateField(auto_now_add=True)
    contact_info = models.CharField(max_length=150, blank=True)

class FoundItemImage(models.Model):
    found_item = models.ForeignKey(FoundItem, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='items/')

class LostItemImage(models.Model):
    lost_item = models.ForeignKey(LostItem, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='items/')
