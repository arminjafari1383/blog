from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django_resized import ResizedImageField
from django.template.defaultfilters import slugify


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
    reading_time = models.PositiveIntegerField(verbose_name="زمان مطالعه")


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
    
    def save(self,*args,**kwargs):
        if not self.args:
            self.slug = slugify(self.title)
        super().save(*args,**kwargs)


class Ticket(models.Model):
    message = models.TextField(verbose_name="پیام")
    name = models.CharField(max_length=250,verbose_name="نام")
    email = models.EmailField(verbose_name="ایمیل")
    phone = models.CharField(max_length=11,verbose_name="شماره تماس")
    subject = models.CharField(max_length=250,verbose_name="موضوع")



    def __str__(self):
        return self.name

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments",verbose_name="پست")
    name = models.CharField(max_length=250,verbose_name="نام")
    body = models.TextField(verbose_name="متن کامنت")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)
    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت ها"
    def __str__(self):
        return f"{self.name}؛ {self.post}"
    

class Image(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="images",verbose_name="تصویر")
    image_file = ResizedImageField(upload_to="post_images/",size = [500,500],quality = 75,crop = ['middle','center'])
    title = models.CharField(max_length=250,verbose_name="عنوان",null=True,blank=True)
    description = models.TextField(verbose_name="توضیحات",null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]
        verbose_name = "تصویر"
        verbose_name_plural = "تصویر ها"
    def __str__(self):
        return self.title
