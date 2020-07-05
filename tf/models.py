from django.db import models
from django.urls import reverse

class Video(models.Model):
	video = models.FileField()

	def get_absolute_url(self):
		return reverse('tf:afterupload')