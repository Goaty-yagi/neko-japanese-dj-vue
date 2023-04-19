from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import Http404
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings

# from django.contrib.auth.models import User as AuthUser
from uuid import uuid4
from datetime import timezone
from allauth.account.models import EmailAddress
import datetime
from django.utils import timezone
from allauth.socialaccount.models import SocialAccount


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        print("CU", self)
        if not email:
            raise ValueError('email is required')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.last_login = datetime.datetime.now() 

        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user
        


class User(AbstractBaseUser, PermissionsMixin):
    UID = models.CharField(max_length=255, default=uuid4, primary_key=True, unique=True, editable=False)
    username = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    thumbnail = models.ImageField(blank=True, null=True, default='account/default.png')
    sns_thumbnail = models.CharField(max_length=255, default='', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    test_taken = models.BooleanField(default=False)
    test_taken_at = models.DateTimeField(auto_now_add=True, blank=False)
    date_offset = models.IntegerField(default=0)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['-created_on',]

    def get_thumbnail(self):
        if self.sns_thumbnail:
            return settings.HOST + self.sns_thumbnail.url
        elif self.thumbnail:
            return settings.HOST + self.thumbnail.url
        return ''        

    def __str__(self):
        return self.username

# class User(models.Model):
#     user = models.OneToOneField(AuthUser, on_delete=models.CASCADE, default=None)
#     UID = models.CharField(max_length=100, primary_key=True)
#     name = models.CharField(max_length=20)
#     email = models.EmailField(blank=False)
#     country = models.CharField(max_length=100, blank=True, null=True)
#     thumbnail = models.ImageField(blank=True, null=True, default='account/default.png')
#     created_on = models.DateTimeField(auto_now_add=True, blank=True)

#     class Meta:
#         ordering = ['-created_on',]

    # def __str__(self):
    #     return self.name


class IPData(models.Model):
    user = models.ForeignKey(User,null=True,related_name='ip_data', on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    ip = models.CharField(max_length=100)
    loc = models.CharField(max_length=100)
    org = models.CharField(max_length=100)
    postal = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    timezone = models.CharField(max_length=100)

    # def save(self, *args, **kwargs):
    #     print('ip_save',self.user.id)
    #     if self.user.country == False:
    #         self.user.country = self.country
    #         super().save(*args, **kwargs)
    


@receiver(post_save, sender=EmailAddress)
def handle_verification(sender, instance, created, **kwargs): 
    if created == True:
        user = User.objects.get(email=instance.email)
        print("CREATED",sender,"IN",instance, "USxs",user,instance.email)
        if user.is_staff:
            return None
        if not instance.verified:
            user.is_active = False
            user.save()


@receiver(post_save, sender=SocialAccount)
def handle_verification(sender, instance, created, **kwargs):
    # need to think about root of media
    if created == True:
        user = User.objects.get(UID=instance.user_id)
        user.sns_thumbnail = instance.extra_data.get("picture")
        user.save()
        
            
            
@receiver(post_save, sender=IPData)
def handle_on_reply(sender, instance, created, **kwargs):
    print('IIIInstance',instance,'cCCCreated',created, 'SSSsender',sender)  
    if created == True:
        print("CREATED",instance.country)
        try:
            user = User.objects.get(UID=instance.user.UID)
            if user.country:
                None
            else:
                user.country = instance.country
                user.save()
        except:
            raise Http404

# @receiver(post_save, sender=AuthUser)
# def handle_on_reply(sender, instance, created, **kwargs):
#     print('AUTHUSER__IIIInstance',instance,'cCCCreated',created, 'SSSsender',sender)  
#     if created == True:
#         print("CREATED")
#         try:
#             user = User.objects.get(UID=instance.user.UID)
#             if user.country:
#                 None
#             else:
#                 user.country = instance.country
#                 user.save()
#         except:
#             raise Http404