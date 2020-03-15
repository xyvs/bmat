from django.db import models


class Channel(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Performer(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Song(models.Model):
    title = models.CharField(max_length=255)
    performer = models.ForeignKey(Performer, on_delete=models.CASCADE, related_name="songs")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'performer'],
                name='Unique title per performer'
            )
        ]


class Play(models.Model):
    title = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='plays')
    performer = models.ForeignKey(Performer, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'performer', 'channel', 'start'],
                name='A channel can have the same date just once'
            )
        ]
