from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.

class TimeIt(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Message(TimeIt):
    user_from = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    message = models.TextField()
    room = models.ForeignKey('Room', on_delete=models.CASCADE)

    def __str__(self):
        return self.user_from.username


class Room(TimeIt):
    name = models.CharField(max_length=30)
    users = models.ManyToManyField(get_user_model())

    def __str__(self):
        return self.name
