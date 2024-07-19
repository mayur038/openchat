from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.db.models.signals  import post_save
from django.core.mail.backends.smtp import EmailBackend
from django.dispatch import receiver
from uuid import uuid4
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User

# from django.contrib.auth import get_user_model
# User = get_user_model()
class cuser(AbstractUser):  
    phone = models.CharField(max_length=11, unique=True, default='null')
    user_profile = models.ImageField(upload_to="profile", default='null')
    verified = models.BooleanField(default=False)    
    
    REQUIRED_FIELDS = ['phone','email']
    objects = UserManager()

    def __str__(self):
        return self.phone

class Box(models.Model):
    username = models.ForeignKey(cuser,on_delete=models.CASCADE)
    people = models.IntegerField(default= 1,max_length=2)
    chatcode = models.CharField(max_length=6)
class Messages(models.Model):
    username = models.ForeignKey(cuser,on_delete=models.CASCADE)
    Message = models.TextField(max_length=2000,default='null')
    Time = models.DateTimeField()
    chatcode = models.ForeignKey(Box,on_delete=models.CASCADE)




# @receiver(post_save, sender=cuser)
# def send_email_token(sender, instance, created, **kwargs):
#     if created:
#         try:
#             subject = 'subject one'
#             id = str(uuid4())
#             message = (
#                 "Thank you for Registration.. \n it's m. \n Your panoti has been started succesfully.."
#             )
#             Email_from = settings.EMAIL_HOST_USER
#             r_list = [instance.email]

#             # Debugging statements
#             print(f"Recipient List: {r_list}")
#             if not r_list:
#                 raise ValueError("Recipient list is empty. Email not sent.")

#             send_mail(subject, message, Email_from, r_list)
#             print("Email sent successfully")
#         except Exception as e:
#             print(f"Error sending email: {e}")
