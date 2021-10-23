from django.db import models

class Images(models.Model):
    image = models.ImageField(upload_to='media/images/', blank=True)


class PDFile(models.Model):
    file = models.FileField(upload_to='media/')
    number = models.IntegerField(default=0)
    images = models.ManyToManyField(Images, blank=True)
    # edited_file = models.FileField(upload_to='media/', blank=True)
    # upload_time = models.DateTimeField(blank=True)
    # download_counter = models.PositiveIntegerField(blank=True)
    # user_ip = models.GenericIPAddressField()


