from django import forms
from .models import Poll, Choice


class EditPollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['poll_text',]
        widgets = {
            'poll_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'columns': 20, }),
        }


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text',]
        widgets = {
            'choice_text': forms.TextInput(attrs={'class': 'form-control', }),
        }
