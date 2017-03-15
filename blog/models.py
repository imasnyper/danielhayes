from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

def image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<blog-title>/images/<filename>
    return 'images/{0}/{1}'.format(instance.image_title, filename)


class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        )
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    post = models.TextField()
    pub_date = models.DateTimeField('date published', default=timezone.now)

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
