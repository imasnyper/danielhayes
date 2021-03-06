from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from tinymce import models as tinymce_models


def image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/images/<filename>
    return 'images/{0}'.format(filename)


class Tag(models.Model):
    alphanumeric = RegexValidator(
        r'[0-9a-zA-Z]*$', 'Only alphanumeric characters will be allowed')
    tag = models.CharField(max_length=25, validators=[alphanumeric])
    slug = models.SlugField(unique=True)

    def tag_post_count(self):
        return len(self.post_set.filter(pub_date__lte=timezone.now()))

    def total_post_count(self):
        return len(Post.objects.filter(pub_date__lte=timezone.now()))

    def frequency(self):
        tag_post_num = self.tag_post_count()
        all_posts_num = self.total_post_count()
        return tag_post_num / all_posts_num

    def save(self, *args, **kwargs):
        Tag.full_clean(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.tag


class Post(models.Model):
    slug_validator = RegexValidator(
        r'[0-9a-zA-Z\-\_]*$',
        'Only alphanumeric character and "-" and "_" will be allowed'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, validators=[slug_validator])
    post = tinymce_models.HTMLField()
    pub_date = models.DateTimeField('date published', default=timezone.now)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', args=[self.slug])


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
