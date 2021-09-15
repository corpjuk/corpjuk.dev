from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils import timezone

from .utils import slugify_instance_title

# Create your models here.
# https://docs.djangoproject.com/en/3.2/ref/models/fields/#model-field-types
# Model Fields Documentation


class Article(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateField(auto_now_add=False,auto_now=False, default=timezone.now, blank=True)
     # null=true, blank=true. null means in db it can be empty value, blank means on forms/admin it can be empty value

    def save(self, *args, **kwargs):
        #set something 
        # if self.slug is None:
        #     self.slug = slugify(self.title)
        # if self.slug is None:
        #     slugify_instance_title(self, save=False)
        super().save(*args, **kwargs)
        # do another something

def article_pre_save(sender, instance, *args, **kwargs):
    #pre save - saves before the save signal
    print('pre_save')
    #print(sender, instance) #good to know and for future use
    if instance.slug is None:
        slugify_instance_title(instance, save=False)

pre_save.connect(article_pre_save, sender=Article)

def article_post_save(sender, instance, created, *args, **kwargs):
    #post save - saves after the save signal
    print('post_save')
    #print(args, kwargs)
    if created:
        slugify_instance_title(instance, save=True)
post_save.connect(article_post_save, sender=Article)