from django import forms

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
    skill = forms.ModelChoiceField(label='Skill', queryset=Skill.objects.all(), required=True, error_messages={'error_duplicate': 'Competency with this Skill already exists, edit it from your profile page'})
    interest = forms.ChoiceField(label='Interest', choices=Competency.INTEREST_CHOICES)
    experience = forms.ChoiceField(label='Experience', choices=Competency.EXPERIENCE_CHOICES)

    def __init__(self, *args, **kwargs):
        self.employee = kwargs.pop('employee')  # cache the user object you pass in
        super(CompetencyForm, self).__init__(*args, **kwargs)  # and carry on to init the form

    def clean_skill(self):
        competencies = self.employee.competencies.all()
        # Make sure that the user does not create a competency with a skill they have already registered
        for competency in competencies:
            if self.cleaned_data['skill'] == competency.skill:
                raise forms.ValidationError(self.fields['skill'].error_messages['error_duplicate'])

        return self.cleaned_data['skill']
