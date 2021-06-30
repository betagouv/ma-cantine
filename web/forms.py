import re
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django import forms
from django.utils.safestring import mark_safe
from data.models import Canteen
from data.models import Sector


class RegisterForm(UserCreationForm):
    cgu_approved = forms.BooleanField(
        label=mark_safe(
            'J\'atteste avoir lu et accepté les <a href="/cgu" target="_blank">CGU</a>'
        )
    )
    email = forms.EmailField()
    canteen_name = forms.CharField(label="Nom de la cantine")
    siret = forms.CharField(label="SIRET", required=False)

    autocomplete = forms.CharField(label="Ville / Région")
    city = forms.CharField(widget=forms.HiddenInput())
    department = forms.CharField(widget=forms.HiddenInput())
    city_insee_code = forms.CharField(widget=forms.HiddenInput())
    postal_code = forms.CharField(widget=forms.HiddenInput())

    sectors = forms.MultipleChoiceField(label="Secteurs d'activité", widget=forms.CheckboxSelectMultiple)
    daily_meal_count = forms.IntegerField(label="Nombre de repas moyen par jour")
    management_type = forms.ChoiceField(
        label="Mode de gestion",
        choices=(("direct", "Directe"), ("conceded", "Concédée")),
        widget=forms.RadioSelect,
    )

    uses_columns = True

    class Meta:  
        model = get_user_model()
        fields = "__all__"

    def left_column_fields(self):
        field_names = [
            "first_name",
            "last_name",
            "email",
            "username",
            "password1",
            "password2",
        ]
        return [next(field for field in self if field.name == field_name) for field_name in field_names]

    def right_column_fields(self):
        field_names = [
            "canteen_name",
            "siret",
            "autocomplete",
            "daily_meal_count",
            "sectors",
            "management_type",
        ]
        return [next(field for field in self if field.name == field_name) for field_name in field_names]

    def hidden_fields(self):
        return [field for field in self if field.is_hidden]

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields["first_name"].widget.attrs.update({"placeholder": "Agnès"})
        self.fields["last_name"].widget.attrs.update({"placeholder": "Dufresne"})
        self.fields["username"].widget.attrs.update({"placeholder": "agnes.dufresne", "autofocus": False})
        self.fields["email"].widget.attrs.update({"placeholder": "agnes.d@example.com"})
        self.fields["canteen_name"].widget.attrs.update({"placeholder": "Ma cantine"})
        self.fields["siret"].widget.attrs.update({"placeholder": "123 456 789 00001"})
        self.fields["autocomplete"].widget.attrs.update({"placeholder": "Sélectionnez une ville "})
        self.fields["sectors"].widget.attrs.update({"class": "sector"})
        self.fields["sectors"].choices = Sector.choices()
        self.fields["management_type"].widget.attrs.update({"class": "management-type"})
        self.fields["password1"].widget.attrs.update(
            {"placeholder": "Entrez votre mot de passe"}
        )
        self.fields["password2"].widget.attrs.update(
            {"placeholder": "Confirmez votre mot de passe"}
        )

    def clean_autocomplete(self):
        if not self.cleaned_data.get('city_insee_code'):
            raise ValidationError("Veuillez choisir une ville de la liste déroulante")
        return self.cleaned_data["autocomplete"]

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

        if commit:
            user.save()
            canteen = Canteen(
                name=self.cleaned_data.get("canteen_name"),
                siret=self.cleaned_data.get("siret"),
                city=self.cleaned_data.get("city"),
                department=self.cleaned_data.get("department"),
                city_insee_code = self.cleaned_data.get("city_insee_code"),
                postal_code = self.cleaned_data.get("postal_code"),
                daily_meal_count=self.cleaned_data.get("daily_meal_count"),
                management_type=self.cleaned_data.get("management_type"),
            )
            canteen.save()
            canteen.managers.add(user)
            for sector in self.cleaned_data.get("sectors"):
                canteen.sectors.add(sector)

        return user
