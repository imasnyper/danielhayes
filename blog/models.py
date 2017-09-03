from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


def image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/images/<filename>
    # return 'images/{0}/{1}'.format(instance.image_title, filename)
    return 'images/{0}'.format(filename)
    
    
class Tag(models.Model):
    tag = models.CharField(max_length=25)
    
    def __str__(self):
        return self.tag


class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        )
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    post = models.TextField()
    pub_date = models.DateTimeField('date published', default=timezone.now)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title


class PostImage(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        )
    image_title = models.CharField(max_length=30)
    image_height = models.IntegerField()
    image_width = models.IntegerField()
    image = models.ImageField(
        upload_to=image_directory_path,
        width_field='image_width',
        height_field='image_height')

    def __str__(self):
        return self.image_title
