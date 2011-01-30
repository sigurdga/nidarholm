from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from accounts.models import UserProfile
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory, inlineformset_factory
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

class LoginForm(AuthenticationForm):
    username = forms.CharField(label=_("Username"), max_length=30, help_text='%s <a href="%s" tabindex="4">%s</a>' % (_("Are you a new user?"), "/accounts/register/", _("Please register")))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput, help_text='%s <a href="%s" tabindex="5">%s</a>' % (_("No password?"), "/accounts/password/reset/", _("Reset your password")))

class ProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        try:
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
        except User.DoesNotExist:
            pass

    first_name = forms.CharField(label=_("First name"), help_text="")
    last_name = forms.CharField(label=_("Last name"), help_text="")
    email = forms.EmailField(label=_("Primary email"), help_text="")

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'email', 'cellphone', 'address', 'postcode', 'born', 'personal_website', 'occupation', 'employer', 'employer_website')

    def save(self, *args, **kwargs):
        """
        Update the primary email address on the related User object as well.
        """
        u = self.instance.user
        u.email = self.cleaned_data['email']
        u.first_name = self.cleaned_data['first_name']
        u.last_name = self.cleaned_data['last_name']
        u.save()
        profile = super(ProfileForm, self).save(*args, **kwargs)
        return profile

class UserGroupsForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False)

    class Meta:
        model = User
        fields = ('id', 'groups')
