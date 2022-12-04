from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.TextField(blank=True, default='')
    body = models.TextField(blank=True, default='')
    owner = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blogCovers/', blank=True, null=True)
    count = models.BigIntegerField(default=0, null=True, blank=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.title

class VisitedIPs(models.Model):
    ip = models.CharField(max_length=250, blank=True, null=True)
    post = models.ForeignKey(Post, related_name='visited_post', on_delete=models.CASCADE)

    def __str__(self):
        return self.ip

class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    body = models.TextField(blank=False)
    owner = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.owner.username + "-" + self.post.title

class Reaction(models.Model):
    CHOICES = (
        ('Like', 'Like'),
        ('Dislike', 'Dislike')
    )
    created = models.DateTimeField(auto_now_add=True)
    emotion = models.CharField(max_length=200, choices=CHOICES, default='Like', null=True, blank=True)
    owner = models.ForeignKey(User, related_name='reacted_by', on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(Post, related_name='reacted_on', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.emotion + "_by_" + self.owner.username

class Category(models.Model):
    name = models.CharField(max_length=200, blank=False, default='')
    owner = models.ForeignKey(User, related_name='categories', on_delete=models.CASCADE)
    posts = models.ManyToManyField(Post, related_name='categories', blank=True)

    class Meta:
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name