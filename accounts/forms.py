from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms
from django.contrib.auth.models import User

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question', 'dataIn', 'dataOut', 'allowed_libraries', 'company']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class SubmitAnswer(ModelForm):
    class Meta:
        model = Answer
        fields = '__all__'

class CreateCandidateForm(ModelForm):
    class Meta:
        model = User
        fields = ['username']

class CandidateEmailForm(ModelForm):
    class Meta:
        model = CandidatesEmail
        fields = ['email']