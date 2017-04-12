from django.db import models
from django.contrib.auth.models import User

# profile extends (one to one) Django User model. 
# TIP: Use User.objects...select_related('profile') where need both data
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
#    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



#user preferences:
