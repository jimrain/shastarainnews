from django.db import models

class Account(models.Model):
    name = models.CharField(max_length=30)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name


def account_video_media_directory_path(instance, filename):
    print (instance)
    print (filename)
    return '{0}/{1}/{2}'.format(instance.account.id, instance.id, instance.title)


class Video(models.Model):
    title = models.CharField(max_length=30)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField()

    digital_master = models.FileField(upload_to=account_video_media_directory_path, blank=True, null=True)

    def __str__(self):
        return self.title

class Rendition(models.Model):
    name = models.CharField(max_length=20)
    url = models.URLField()
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

    def __str__(self):
        return self.name