from django.db import models
from django.utils.timezone import now
from core.models import Channel,User

# Create your models here.
class Genre(models.TextChoices):
    ACTION = 'Action', 'Action'
    ADVENTURE = 'Adventure', 'Adventure'
    ANIMATION = 'Animation', 'Animation'
    BIOGRAPHY = 'Biography', 'Biography'
    COMEDY = 'Comedy', 'Comedy'
    CRIME = 'Crime', 'Crime'
    DOCUMENTARY = 'Documentary', 'Documentary'
    DRAMA = 'Drama', 'Drama'
    FAMILY = 'Family', 'Family'
    FANTASY = 'Fantasy', 'Fantasy'
    FILM_NOIR = 'Film-Noir', 'Film-Noir'
    HISTORY = 'History', 'History'
    HORROR = 'Horror', 'Horror'
    MUSICAL = 'Musical', 'Musical'
    MYSTERY = 'Mystery', 'Mystery'
    ROMANCE = 'Romance', 'Romance'
    SCI_FI = 'Sci-Fi', 'Sci-Fi'
    SPORT = 'Sport', 'Sport'
    THRILLER = 'Thriller', 'Thriller'
    WAR = 'War', 'War'
    WESTERN = 'Western', 'Western'
    SHORT = 'Short', 'Short'
    MUSIC = 'Music', 'Music'

class Movie(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(
        max_length=20,
        choices=Genre.choices,
        default=Genre.ACTION
    )

    def __str__(self):
        return f"{self.title} ({self.genre})"

class Video(models.Model):
    channel=models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='videos')
    videoFile = models.FileField(upload_to='videos/')  
    date = models.DateTimeField(default=now)  
    title = models.CharField(max_length=255)
    rating = models.FloatField(default=0)
    genre = models.CharField(max_length=20,choices=Genre.choices,default=Genre.ACTION)
    description = models.TextField(blank=True)  
    views = models.PositiveIntegerField(default=0)  
    likes = models.PositiveIntegerField(default=0)
    
    def increment_views(self):
        self.views += 1
        self.save()

    def increment_likes(self):
        self.likes += 1
        self.save()

    def __str__(self):
        return f"{self.title} (Channel: {self.channel.name})"

class VideoRating(models.Model):
    video=models.ForeignKey(Video, related_name="comments", on_delete=models.CASCADE)
    commentor=models.ForeignKey(User, related_name="commentor", on_delete=models.CASCADE)
    rating = models.FloatField(default=0)
    content= models.TextField(max_length=600)
    is_edited = models.BooleanField(default=False)
    date = models.DateTimeField(default=now)
    pinned = models.BooleanField(default=False)
    def __str__(self):
        return f"Comment on {self.video.title} - {self.content[:30]}..."

class ReportVideo(models.Model):
    video = models.ForeignKey(Video,on_delete=models.CASCADE,related_name="video_reports")
    reason = models.TextField()
    video_reporter = models.ForeignKey(User, on_delete=models.CASCADE,related_name="video_reports")
    date = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Report for Video ID {self.video.pk} by {self.video_reporter}"

class ReportRating(models.Model):
    comment = models.ForeignKey(VideoRating,on_delete=models.CASCADE,related_name="rating_reports")
    reason = models.TextField()
    rating_reporter = models.ForeignKey(User, on_delete=models.CASCADE,related_name="rating_reports")
    date = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Report for rating ID {self.comment.pk} by {self.rating_reporter}"