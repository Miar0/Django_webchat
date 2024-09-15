import os.path

from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

def avatar_upload_to(obj, filename):
    return f"avatars/{filename}"


class SocialUser(AbstractUser):
    avatar = models.ImageField(blank=True, upload_to=avatar_upload_to, default='avatar/default.png')
    birthday = models.DateField(blank=True, null=True)
    verify = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.avatar.path)
        # output_size = (50, 50)
        # thumb = img.thumbnail(output_size)
        output_width = 50
        w_percent = output_width / img.size[0]
        output_height = int(img.size[1] * w_percent)
        img = img.resize((output_width, output_height), Image.Resampling.HAMMING)
        thumbnail_path = os.path.join(os.path.dirname(self.avatar.path), f"thumb_{os.path.basename(self.avatar.path)}")
        img.save(thumbnail_path)

    def get_thumbnail_url(self):
        return self.avatar.url.replace('avatars/', 'avatars/thumb_')


class TimeIt(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Message(TimeIt):
    user_from = models.ForeignKey(SocialUser, on_delete=models.CASCADE)
    message = models.TextField()
    room = models.ForeignKey('Room', on_delete=models.CASCADE)

    def __str__(self):
        return self.user_from.username


class Room(TimeIt):
    name = models.CharField(max_length=30)
    users = models.ManyToManyField(SocialUser)

    def get_other_user(self, current_user):
        return self.users.exclude(id=current_user.id).first()

    def __str__(self):
        return self.name


class FriendRequests(TimeIt):
    from_user = models.ForeignKey(SocialUser, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(SocialUser, related_name='to_user', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user} -> {self.to_user}"

    def accept(self):
        self.accepted = True
        self.save()
        room_name = f"{self.from_user} -> {self.to_user}"
        room = Room.objects.create(name=room_name)
        room.users.add(self.from_user, self.to_user)
        return room
