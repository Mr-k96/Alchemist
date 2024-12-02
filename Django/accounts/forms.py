from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django import forms
from .models import TermsAgreement


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()


class TermsAgreementForm(forms.ModelForm):
    class Meta:
        model = TermsAgreement
        fields = ['all_agreed', 'terms_of_service', 'privacy_policy']
        