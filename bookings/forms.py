from django import forms
from .models import Booking, ConversationMessage


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['full_name', 'email', 'phone', 'event_type', 'event_date', 'guests', 'message']
        widgets = {
            'email': forms.EmailInput(attrs={'autocomplete': 'email'}),
            'event_date': forms.DateInput(attrs={'type': 'date'}),
            'guests': forms.NumberInput(attrs={'min': 1}),
            'message': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Tell the vendor about your event...'}),
        }


class ConversationMessageForm(forms.ModelForm):
    class Meta:
        model = ConversationMessage
        fields = ['body']
        widgets = {'body': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write a message about your event...'})}
