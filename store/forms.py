from django import forms
from .models import *


class testingform(forms.ModelForm):
    class Meta:
        model = Website_Info
        fields = '__all__'

class addtocart(forms.ModelForm):
    class Meta:
        model = Product_Details
        fields = '__all__'

class userprofileForm(forms.ModelForm):
    class Meta:
        model = User_Details
        fields = '__all__' 
