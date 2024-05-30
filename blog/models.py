from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='post_photos/')
    date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return self.title

class Paragraph(models.Model):
    post = models.ForeignKey(Post, related_name='paragraphs', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='paragraph_photos/', blank=True, null=True)

    def __str__(self):
        return f'Paragraph of {self.post.title}'
