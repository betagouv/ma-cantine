import re
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.utils.safestring import mark_safe


class RegisterUserForm(UserCreationForm):
    cgu_approved = forms.BooleanField(
        label=mark_safe('J\'atteste avoir lu et accepté les <a href="/cgu" target="_blank">CGU</a>')
    )
    is_dev = forms.BooleanField(required=False)
    email = forms.EmailField()
    creation_mtm_source = forms.CharField(widget=forms.HiddenInput(), required=False)
    creation_mtm_campaign = forms.CharField(widget=forms.HiddenInput(), required=False)
    creation_mtm_medium = forms.CharField(widget=forms.HiddenInput(), required=False)

    uses_columns = True

    class Meta:
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
            "is_dev",
            "email",
            "phone_number",
            "username",
            "password1",
            "password2",
            "cgu_approved",
            "number_of_managed_cantines",
            "creation_mtm_source",
            "creation_mtm_campaign",
            "creation_mtm_medium",
        )

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields["first_name"].widget.attrs.update({"placeholder": "Agnès"}, autoFocus=True)
        self.fields["last_name"].widget.attrs.update({"placeholder": "Dufresne"})
        self.fields["username"].widget.attrs.update({"placeholder": "agnes.dufresne"})
        self.fields["email"].widget.attrs.update({"placeholder": "agnes.d@example.com"})
        self.fields["phone_number"].widget.attrs.update({"placeholder": "0* ** ** ** **"})
        self.fields["password1"].widget.attrs.update({"placeholder": "Entrez votre mot de passe"})
        self.fields["password2"].widget.attrs.update({"placeholder": "Confirmez votre mot de passe"})
        self.fields["number_of_managed_cantines"].widget.attrs.update({"class": "cantine-number-input", "min": "0"})

    def left_column_fields(self):
        field_names = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
        ]
        return [field for field in self if not field.is_hidden and field.name in field_names]

    def right_column_fields(self):
        field_names = [
            "username",
            "password1",
            "password2",
        ]
        return [field for field in self if not field.is_hidden and field.name in field_names]

    def clean_cgu_approved(self):
        return _clean_cgu_approved(self)

    def clean_username(self):
        return _clean_username(self)

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if not phone_number:
            return phone_number
        number = phone_number.replace(" ", "").replace("-", "")
        if len(number) != 10 or not number.isdigit():
            raise forms.ValidationError("Dix chiffres numériques attendus")
        return phone_number

    def save(self, commit=True):
        user = super(RegisterUserForm, self).save(commit=False)
        user.email = get_user_model().objects.normalize_email(self.cleaned_data.get("email"))

        if commit:
            user.save()

        return user


def _clean_cgu_approved(form):
    if not form.cleaned_data.get("cgu_approved"):
        raise forms.ValidationError("Vous devez accepter les conditions d'utilisation")
    return form.cleaned_data["cgu_approved"]


def _clean_username(form):
    # username can't be an email
    username = form.cleaned_data.get("username", "")
    regex = r"(.*)@(.*)\.(.*)"
    match = re.match(regex, username)
    if match is not None:
        raise forms.ValidationError("Vous ne pouvez pas utiliser une adresse email comme nom d'utilisateur.")

    return username
