import re
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.utils.safestring import mark_safe
from data.models import Canteen
from data.models import Sector
from data.department_choices import Department


class RegisterForm(UserCreationForm):
    cgu_approved = forms.BooleanField(
        label=mark_safe(
            'J\'atteste avoir lu et accepté les <a href="/cgu" target="_blank">CGU</a>'
        )
    )
    email = forms.EmailField()
    canteen_name = forms.CharField(label="Nom de la cantine")
    siret = forms.CharField(label="SIRET", required=False)
    city = forms.CharField(label="Ville/Commune")
    department = forms.ChoiceField(label="Département", choices=[(None, '---')] + Department.choices)
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
        fields = (
            "first_name",
            "last_name",
            "email",
            "canteen_name",
            "siret",
            "city",
            "department",
            "daily_meal_count",
            "sectors",
            "management_type",
            "username",
            "password1",
            "password2",
            "cgu_approved",
        )

    def left_column_fields(self):
        field_names = [
            "first_name",
            "last_name",
            "email",
            "username",
            "password1",
            "password2",
        ]
        return [field for field in self if not field.is_hidden and field.name in field_names]

    def right_column_fields(self):
        field_names = [
            "canteen_name",
            "siret",
            "city",
            "department",
            "daily_meal_count",
            "sectors",
            "management_type",
        ]
        return [field for field in self if not field.is_hidden and field.name in field_names]

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields["first_name"].widget.attrs.update({"placeholder": "Agnès"})
        self.fields["last_name"].widget.attrs.update({"placeholder": "Dufresne"})
        self.fields["username"].widget.attrs.update({"placeholder": "agnes.dufresne"})
        self.fields["email"].widget.attrs.update({"placeholder": "agnes.d@example.com"})
        self.fields["canteen_name"].widget.attrs.update({"placeholder": "Ma cantine"})
        self.fields["siret"].widget.attrs.update({"placeholder": "123 456 789 00001"})
        self.fields["city"].widget.attrs.update({"placeholder": "Ville/Commune"})
        self.fields["sectors"].widget.attrs.update({"class": "sector"})
        self.fields["sectors"].choices = Sector.choices()
        self.fields["management_type"].widget.attrs.update({"class": "management-type"})
        self.fields["password1"].widget.attrs.update(
            {"placeholder": "Entrez votre mot de passe"}
        )
        self.fields["password2"].widget.attrs.update(
            {"placeholder": "Confirmez votre mot de passe"}
        )

    def clean_cgu_approved(self):
        return _clean_cgu_approved(self)

    def clean_username(self):
        return _clean_username(self)

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
                daily_meal_count=self.cleaned_data.get("daily_meal_count"),
                management_type=self.cleaned_data.get("management_type"),
            )
            canteen.save()
            canteen.managers.add(user)
            for sector in self.cleaned_data.get("sectors"):
                canteen.sectors.add(sector)

        return user


class RegisterUserForm(UserCreationForm):
    cgu_approved = forms.BooleanField(
        label=mark_safe(
            'J\'atteste avoir lu et accepté les <a href="/cgu" target="_blank">CGU</a>'
        )
    )
    email = forms.EmailField()

    class Meta:  
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
            "email",
            "username",
            "password1",
            "password2",
            "cgu_approved",
        )

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields["first_name"].widget.attrs.update({"placeholder": "Agnès"}, autoFocus=True)
        self.fields["last_name"].widget.attrs.update({"placeholder": "Dufresne"})
        self.fields["username"].widget.attrs.update({"placeholder": "agnes.dufresne"})
        self.fields["email"].widget.attrs.update({"placeholder": "agnes.d@example.com"})
        self.fields["password1"].widget.attrs.update(
            {"placeholder": "Entrez votre mot de passe"}
        )
        self.fields["password2"].widget.attrs.update(
            {"placeholder": "Confirmez votre mot de passe"}
        )

    def clean_cgu_approved(self):
        return _clean_cgu_approved(self)

    def clean_username(self):
        return _clean_username(self)

    def save(self, commit=True):
        user = super(RegisterUserForm, self).save(commit=False)
        user.email = get_user_model().objects.normalize_email(
            self.cleaned_data.get("email")
        )

        if commit:
            user.save()

        return user

def _clean_cgu_approved(form):
    if not form.cleaned_data.get("cgu_approved"):
        raise forms.ValidationError(
            "Vous devez accepter les conditions d'utilisation"
        )
    return form.cleaned_data["cgu_approved"]

def _clean_username(form):
    # username can't be an email
    username = form.cleaned_data.get("username", "")
    regex = r"(.*)@(.*)\.(.*)"
    match = re.match(regex, username)
    if match is not None:
        raise forms.ValidationError(
            "Vous ne pouvez pas utiliser une adresse email comme nom d'utilisateur."
        )

    return username
