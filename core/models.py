from django.db import models

class Favorite(models.Model):
    CATEGORY_CHOICES = [
        ('movie', 'Movie'),
        ('sports', 'Sports'),
        ('restaurant', 'Restaurant'),
        ('event', 'Event'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=200)
    date = models.CharField(max_length=100, blank=True, null=True)
    time = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name