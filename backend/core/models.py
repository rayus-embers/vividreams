from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image

# Create your models here.
class User(AbstractUser):
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.username

class Channel(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="creator_profile")
    name = models.CharField(max_length=50, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    instagram = models.URLField(max_length=80, blank=True, null=True)
    facebook = models.URLField(max_length=80, blank=True, null=True)
    tiktok = models.URLField(max_length=80, blank=True, null=True)
    x = models.URLField(max_length=80, blank=True, null=True, verbose_name="Twitter/X")
    youtube = models.URLField(max_length=80, blank=True, null=True)
    subscribers = models.ManyToManyField(User, related_name="subscriptions", blank=True)

    def __str__(self):
        return self.name
    
    @property
    def subscriber_count(self):
        return self.subscribers.count()
    #resizing the image
    def save(self, *args, **kwargs):
    # Call the parent class's save method with all arguments
        super().save(*args, **kwargs)

    # Check if the pfp exists
        if self.profile_picture:
            try:
                pic = Image.open(self.profile_picture.path)

                if pic.height > 300:
                    output_size = (200, 90)
                    pic.thumbnail(output_size)
                    pic.save(self.profile_picture.path)
            except Exception as e:
                print(f"Error processing the image: {e}")
    