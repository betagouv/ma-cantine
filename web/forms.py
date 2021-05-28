import re
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.utils.safestring import mark_safe
from data.models import Canteen


class RegisterForm(UserCreationForm):
    cgu_approved = forms.BooleanField(
        label=mark_safe(
            'J\'atteste avoir lu et accepté les <a href="/cgu" target="_blank">CGU</a>'
        )
    )
    email = forms.EmailField()
    canteen_name = forms.CharField(label="Nom de la cantine")

    class Meta:
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
            "email",
            "canteen_name",
            "username",
            "password1",
            "password2",
            "cgu_approved",
        )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields["first_name"].widget.attrs.update({"placeholder": "Agnès"})
        self.fields["last_name"].widget.attrs.update({"placeholder": "Dufresne"})
        self.fields["username"].widget.attrs.update({"placeholder": "agnes.dufresne"})
        self.fields["email"].widget.attrs.update({"placeholder": "agnes.d@example.com"})
        self.fields["canteen_name"].widget.attrs.update({"placeholder": "Ma cantine"})
        self.fields["password1"].widget.attrs.update(
            {"placeholder": "Entrez votre mot de passe"}
        )
        self.fields["password2"].widget.attrs.update(
            {"placeholder": "Confirmez votre mot de passe"}
        )

    def clean_cgu_approved(self):
        if not self.cleaned_data.get("cgu_approved"):
            raise forms.ValidationError(
                "Vous devez accepter les conditions d'utilisation"
            )
        return self.cleaned_data["cgu_approved"]

    def clean_username(self):
        # username can't be an email
        username = self.cleaned_data.get("username", "")
        regex = r"(.*)@(.*)\.(.*)"
        match = re.match(regex, username)
        if match is not None:
            raise forms.ValidationError(
                "Vous ne pouvez pas utiliser une adresse email comme nom d'utilisateur."
            )

        return username

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = get_user_model().objects.normalize_email(
            self.cleaned_data.get("email")
        )
        user.is_active = False

        if commit:
            user.save()
            canteen = Canteen(name=self.cleaned_data.get("canteen_name"))
            canteen.save()
            canteen.managers.add(user)

        return user
