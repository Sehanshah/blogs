from django.db import models


# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    publish_date = models.DateField(null=True)
    author = models.CharField(max_length=100)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    text = models.CharField(max_length=100)
