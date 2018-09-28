from django.db import models


class Slide(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    upload = models.FileField(upload_to='slides/')

    def __str__(self):
        return self.upload.name


class SlidePacket(models.Model):
    description = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.description
