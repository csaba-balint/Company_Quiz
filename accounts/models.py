from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Company(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    question = models.CharField(max_length=300, null=True)
    dataIn = models.CharField(max_length=100, null=True)
    dataOut = models.CharField(max_length=100, null=True)
    allowed_libraries = models.CharField(max_length=100, null=True)
    company = models.ForeignKey(Company, null=True, on_delete=models.SET_NULL)

class Candidate(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    company = models.ForeignKey(Company, null=True, on_delete=models.SET_NULL)

class Answer(models.Model):
    text = models.CharField(max_length=100, null=False)
    question = models.ForeignKey(Question, null=True, on_delete=models.SET_NULL)
    candidate = models.ForeignKey(Candidate, null=True, on_delete=models.SET_NULL)

class CandidatesEmail(models.Model):
    email = models.CharField(max_length=100, null=False)

@receiver(post_save, sender=settings.COMPANY_USER_MODEL)
def create_token(sender, instance, created=False, **kwargs):
    if created:
        print(instance.user)
        Token.objects.create(user=instance.user)





