from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'categories/{self.slug}'


class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Title')
    description = models.TextField(verbose_name='Description')
    slug = models.SlugField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, )
    image = models.ImageField(upload_to='blogimages')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Blogs'

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    def get_absolute_url(self):
        return reverse('detail', args=[str(self.slug)])


class Hashtags(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, blank=True, null=True)
    posts = models.ManyToManyField(Blog, )

    class Meta:
        verbose_name_plural = 'Hashtags'

    def __str__(self):
        return self.name


class PicturesFromTheBlog(models.Model):
    owner = models.ForeignKey(Blog, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='shotsinblogs')

    class Meta:
        verbose_name_plural = 'Pictures from the blog'


class Comment(models.Model):
    post = models.ForeignKey(Blog, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    reply=models.ForeignKey('self',null=True, blank=True, related_name="replies", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
