from django.db import models

# Create your models here.
class Blurb(models.Model):
    title = models.CharField(max_length=30)
    text = models.TextField()
    order_num = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.title