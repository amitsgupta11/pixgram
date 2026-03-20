"""
accounts/forms.py
Forms for user registration and profile editing.
"""
 
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
 
 
class SignupForm(UserCreationForm):
    """Extended signup form that also collects email."""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email address'})
    )
 
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes and placeholders to every field
        placeholders = {
            'username': 'Choose a username',
            'email': 'Email address',
            'password1': 'Password',
            'password2': 'Confirm password',
        }
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-lg'
            field.widget.attrs['placeholder'] = placeholders.get(field_name, '')
            field.help_text = None  # Hide Django's default help text
 
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email
 
 
class ProfileUpdateForm(forms.ModelForm):
    """Allows a user to update their bio and avatar."""
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write something about yourself…'
            }),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }
 
 
class UserUpdateForm(forms.ModelForm):
    """Allows updating the User's first/last name and email."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }