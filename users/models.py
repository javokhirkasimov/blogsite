from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=80, null=True, blank=True)
    last_name = models.CharField(max_length=80, null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_imgs',null=True, blank=True)
    bio = models.TextField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('my_profile')


@receiver(post_save, sender=User)
def create_profile(instance, created, **kwargs):
    if created:
        p = Profile.objects.create(user=instance)
        p.save()

@receiver(post_save, sender=User)
def update_profile(instance, created, **kwargs):
    if created == False:
        instance.profile.save()


# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
# post_save.connect(create_profile, sender=User)

# def update_profile(sender, instance, created, **kwargs):
#     if created == False:
#         instance.profile.save()
# post_save.connect(update_profile, sender=User)