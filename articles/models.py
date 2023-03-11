from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.utils import timezone
from django.urls import reverse
from .utils import slugify_instance_title

# Create your models here.
# https://docs.djangoproject.com/en/3.2/ref/models/fields/#model-field-types
# Model Fields Documentation
User = settings.AUTH_USER_MODEL

class ArticleQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == "":
            return self.none() #this is the same as Article.objects.none(), but it's still an empty list []
        lookups = Q(title__icontains=query) | Q(content__icontains=query)
        return Article.objects.filter(lookups)

class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)
    def search(self, query=None):
        return self.get_queryset().search(query=query)

        # if query is None or query == "":
        #     return self.get_queryset().none() #this is the same as Article.objects.none(), but it's still an empty list []
        # lookups = Q(title__icontains=query) | Q(content__icontains=query)
        # return self.get_queryset().filter(lookups)

class Article(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateField(auto_now_add=False,auto_now=False, default=timezone.now, blank=True)
     # null=true, blank=true. null means in db it can be empty value, blank means on forms/admin it can be empty value

    objects = ArticleManager()

    @property
    def name(self):
        return self.title

    def get_absolute_url(self):
        # return f'/articles/{self.slug}'
        return reverse("articles:detail", kwargs={"slug": self.slug})

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
    #print('pre_save')
    #print(sender, instance) #good to know and for future use
    if instance.slug is None:
        slugify_instance_title(instance, save=False)

pre_save.connect(article_pre_save, sender=Article)

def article_post_save(sender, instance, created, *args, **kwargs):
    #post save - saves after the save signal
    #print('post_save')
    #print(args, kwargs)
    if created:
        slugify_instance_title(instance, save=True)
post_save.connect(article_post_save, sender=Article)