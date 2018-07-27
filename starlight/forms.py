from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import PasswordInput

from starlight.models import Competency, Skill, Employee


class EditForm(forms.ModelForm):
    class Meta:
        model = Competency
        fields = ['interest', 'experience']
    interest = forms.ChoiceField(label='Interest', choices=Competency.INTEREST_CHOICES)
    experience = forms.ChoiceField(label='Experience', choices=Competency.EXPERIENCE_CHOICES)


class CompetencyForm(forms.ModelForm):
    class Meta:
        model = Competency
        fields = ['skill', 'interest', 'experience']
    skill = forms.ModelChoiceField(label='Skill', queryset=Skill.objects.all(), required=True)
    interest = forms.ChoiceField(label='Interest', choices=Competency.INTEREST_CHOICES)
    experience = forms.ChoiceField(label='Experience', choices=Competency.EXPERIENCE_CHOICES)

    def __init__(self, *args, **kwargs):
        self.employee = kwargs.pop('employee')  # cache the user object you pass in
        super(CompetencyForm, self).__init__(*args, **kwargs)  # and carry on to init the form


class EmployeeForm(UserCreationForm):
    class Meta:
        model = Employee
        fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name']
    username = forms.CharField(label='Username', max_length=75, required=True)
    password1 = forms.CharField(widget=PasswordInput(), required=True)
    password2 = forms.CharField(widget=PasswordInput(), required=True, error_messages={'error_matching': 'Passwords do not match!'})
    email = forms.EmailField(max_length=150, required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    def clean_password2(self):
        if not self.cleaned_data['password1'] == self.cleaned_data['password2']:
            raise forms.ValidationError(self.fields['password2'].error_messages['error_matching'])

        return self.cleaned_data['password2']
