from django.db import models

# Create your models here.
class upload(models.Model):
	email = models.EmailField(max_length=50)
	image = models.ImageField(upload_to = 'upload')
	