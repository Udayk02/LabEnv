from django import forms
from django.contrib.auth.models import User
from .models import ClassRoom
from django_select2.forms import ModelSelect2Widget,Select2MultipleWidget   
from django_select2 import forms as s2forms



from django.contrib.admin.widgets import AdminDateWidget,AdminTimeWidget,AdminSplitDateTime


class create_class_form(forms.Form):
    subject = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Subject Name'}))
    classname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Class Name'}))
    
class add_answer_form(forms.Form):
    answer = forms.CharField(widget=forms.Textarea(
        attrs={ 'placeholder': 'Add an answer','class':'answer_text_area'}))


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

#adding participants into class room
class ParticipantsForm(forms.Form):
    lst = []
    choices = []
    def ParticipantsForm(self,pk):
        for student in ClassRoom.objects.get(id=pk).students:
            self.lst.append(student)
    for obj in User.objects.all():
        if obj not in lst:
            choices.append((obj.username, obj.username))
    
    # choices = [(obj.username, obj.username) for obj in User.objects.all()]
    students = forms.MultipleChoiceField(widget=Select2MultipleWidget(attrs={'placeholder': 'Enter Subject Name'}),
                choices=choices)

class create_poll_form(forms.Form):
    option_1 = forms.CharField(required=False,widget=forms.TextInput(
        attrs={'placeholder': 'Enter Option 1'}))
    option_2 = forms.CharField(required=False,widget=forms.TextInput(
        attrs={'placeholder': 'Enter Option 2'}))
    option_3 = forms.CharField(required=False,widget=forms.TextInput(
        attrs={'placeholder': 'Enter Option 3'}))
    option_4 = forms.CharField(required=False,widget=forms.TextInput(
        attrs={'placeholder': 'Enter Option 4'}))
    option_5 = forms.CharField(required=False,widget=forms.TextInput(
        attrs={'placeholder': 'Enter Option 5'}))
    
    