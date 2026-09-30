from django import forms
from django.contrib.auth.models import User
from .models import Voter, Election, Candidate

class VoterRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Voter
        fields = ["voter_id", "name", "email", "password", "confirm_password",
                  "mobile", "dob", "age", "gender", "address"]
        widgets = {"dob": forms.DateInput(attrs={"type": "date"})}

    def clean(self):
        data = super().clean()
        if data.get("password") != data.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match.")
        if Voter.objects.filter(email=data.get("email")).exists():
            raise forms.ValidationError("Email is already registered.")
        if Voter.objects.filter(voter_id=data.get("voter_id")).exists():
            raise forms.ValidationError("Voter ID is already registered.")
        return data

    def save(self, commit=True):
        voter = super().save(commit=False)
        voter.set_password(self.cleaned_data["password"])
        if commit:
            voter.save()
        return voter

class ElectionForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = ["title", "description", "start_date", "end_date", "status"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ["name", "party_name", "party_symbol", "photo", "election", "description", "status"]
