from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


class UserProfile(models.Model):

    ROLE_CHOICES = (
	    ('st', 'Student'),
        ('in', 'Instructor'),
    )
    user = models.OneToOneField(User)
    role = models.CharField(max_length = 2, choices = ROLE_CHOICES, blank = True, null = True, default = 'st')

    def __str__(self):  
          return "%s's profile" % self.user  

def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
       profile, created = UserProfile.objects.get_or_create(user=instance)  

post_save.connect(create_user_profile, sender=User)