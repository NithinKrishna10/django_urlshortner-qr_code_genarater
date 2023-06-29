from django.db import models

# Create your models here.
from django.db import models

class Url(models.Model):
    link = models.CharField(max_length=1000)
    uuid = models.CharField(max_length=10)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)

    def __str__(self):
        return self.link
