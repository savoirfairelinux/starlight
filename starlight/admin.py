from django import forms
from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserChangeForm, UserCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from starlight.models import Skill, Competency, Employee, Team


class MyUserCreationForm(UserCreationForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Employee
        fields = '__all__'

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class MyUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field."""

    password = ReadOnlyPasswordHashField(help_text="Raw passwords are not stored, so there is no way to see this "
                                                   "user's password, but you can change the password using "
                                                   "<a href=\"../password/\">this form</a>.")

    class Meta:
        model = Employee
        exclude = ['password1', 'password2']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'email', 'first_name',
                       'last_name', 'teams', 'user_permissions', 'competencies')}
         ),
    )
    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2', 'email', 'first_name',
                       'last_name', 'teams', 'user_permissions', 'competencies')}
         ),
    )


admin.site.register(Skill)
admin.site.register(Competency)
admin.site.register(Employee, UserAdmin)
admin.site.register(Team)
