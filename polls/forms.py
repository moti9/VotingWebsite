from django import forms
from .models import Poll, Choice,Contact


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


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']

    # Add Bootstrap classes to form widgets
    widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control'}),
        'email': forms.EmailInput(attrs={'class': 'form-control'}),
        'subject': forms.TextInput(attrs={'class': 'form-control'}),
        'message': forms.Textarea(attrs={'class': 'form-control'}),
    }