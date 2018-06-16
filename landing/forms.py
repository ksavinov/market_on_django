from django import forms
from .models import *

class SubscriberForm(forms.ModelForm):

    class Meta:
        model = Subscriber
        # fileds = [""] поля, которые необходимо включить
        exclude = [""]