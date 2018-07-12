from django import forms

from starlight.models import Competency


class ObjectForm(forms.ModelForm):
    class Meta:
        model = Competency
        fields = ['interest', 'experience']
    interest = forms.ChoiceField(label='Interest', choices=Competency.INTEREST_CHOICES)
    experience = forms.ChoiceField(label='Experience', choices=Competency.EXPERIENCE_CHOICES)

