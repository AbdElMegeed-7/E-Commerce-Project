from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
  first_name = forms.CharField(max_length=255, required=True)
  last_name = forms.CharField(max_length=255, required=True)
  email = forms.EmailField(max_length=255, help_text="eg. YourEmail@gmail.com")
  
  class Meta:
    model = User
    fields = ('first_name', 'last_name', 'username', 'password1', 'password2', 'email')
    
    
class ContactForm(forms.Form):
  subject = forms.CharField(max_length=255, required=True)
  name = forms.CharField(max_length=255, required=True)
  from_email = forms.EmailField(max_length=255, required=True)
  message = forms.CharField(max_length=255,
                            widget = forms.Textarea(),
                            help_text="Write here your message"
                            )
  
  
  