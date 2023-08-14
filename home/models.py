from django.db import models

# Create your models here.
class UpLoadImg(models.Model):
    img = models.ImageField(upload_to='img')
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
