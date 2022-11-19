from django import forms
from .models import ClassRoom
# from django.forms.widgets import SplitDateTimeField

from django.contrib.admin.widgets import AdminDateWidget,AdminTimeWidget,AdminSplitDateTime


class create_class_form(forms.Form):
    subject = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Subject Name'}))
    classname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Class Name'}))


class create_assignment_form(forms.Form):
    types = [('post','Post'),('poll','Poll'),('assignment','Assignment')]
    question = forms.CharField(widget=forms.Textarea(
        attrs={ 'placeholder': 'Enter Question'}))
    type = forms.CharField(label='Question Type', 
            widget=forms.Select(
                choices=types, 
                attrs={'placeholder': 'Choose type'}))
    due_date = forms.DateField(widget=AdminDateWidget(attrs={'type': 'date'}))
    due_time = forms.TimeField(widget=AdminTimeWidget(attrs={'type': 'time'}))