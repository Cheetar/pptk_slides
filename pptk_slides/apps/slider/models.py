from django.db import models


class SlidePacket(models.Model):

    description = models.CharField(max_length=150, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description


class Slide(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    upload = models.FileField(upload_to='slides/')
    slide_packet = models.ForeignKey(SlidePacket, on_delete=models.CASCADE)

    def __str__(self):
        return self.upload.name
