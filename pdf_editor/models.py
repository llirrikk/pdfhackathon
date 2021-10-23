from django.db import models


class PDFile(models.Model):
    file = models.FileField(upload_to='media/')
    # edited_file = models.FileField(upload_to='media/', blank=True)
    # upload_time = models.DateTimeField(blank=True)
    # download_counter = models.PositiveIntegerField(blank=True)
    # user_ip = models.GenericIPAddressField()


