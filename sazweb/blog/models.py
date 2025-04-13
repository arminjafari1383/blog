from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

#Mangers
class PublishedManger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status = Post.Status.PUBLISHED)

# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
       DRAFT = 'DF','Draft'
       PUBLISHED = 'PB','Published'
       REJECTED  = 'RJ','Rejected'
    # relations
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_posts")
    # data fields
    title = models.CharField(max_length = 250)
    description = models.TextField()
    slug = models.SlugField(max_length=250)
    # data
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now=True)
    # choices fields
    status = models.CharField(max_length= 2,choices=Status.choices,default=Status.DRAFT)

    objects = models.Manager()
    published = PublishedManger()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail',args=[self.id])

class Ticket(models.Model):
    message = models.TextField(verbose_name="پیام")
    name = models.CharField(max_length=250,verbose_name="نام")
    email = models.EmailField(verbose_name="ایمیل")
    phone = models.CharField(max_length=11,verbose_name="شماره تماس")
    subject = models.CharField(max_length=250,verbose_name="موضوع")



    def __str__(self):
        return self.name
    