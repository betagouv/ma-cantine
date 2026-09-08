import csv
import datetime
import json
from decimal import Decimal

from django.core.serializers.json import DjangoJSONEncoder
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Q


class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super().default(o)


def has_charfield_missing_query(field_name: str):
    return Q(**{f"{field_name}__isnull": True}) | Q(**{f"{field_name}": ""}) | Q(**{f"{field_name}": None})


def has_arrayfield_missing_query(field_name: str):
    return Q(**{f"{field_name}__isnull": True}) | Q(**{f"{field_name}__len": 0}) | Q(**{f"{field_name}": None})


def array_overlap_query(field_name: str, values: list):
    """
    For ArrayField, we can use __overlap with a list of values
    But if the array is in a JSONField, we need to build a __contains OR query for each value.
    """
    query = Q()
    for value in values:
        query |= Q(**{f"{field_name}__contains": [value]})
    return query


def get_diagnostic_lowest_limit_year():
    return 2019


def get_diagnostic_lower_limit_year():
    return datetime.datetime.now().date().year - 1


def get_diagnostic_upper_limit_year():
    return datetime.datetime.now().date().year + 1


def make_optional_positive_integer_field(**kwargs):
    """
    IntegerField with
    - min: 0
    - max: 999999999
    - examples: None, 0, 10, 999999999
    """
    return models.IntegerField(
        blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(999999999)], **kwargs
    )


def make_optional_positive_decimal_field(**kwargs):
    """
    DecimalField with
    - 20 digits, including 2 decimals
    - min: 0
    - max: 999999999999999999.99
    - examples: None, 0, 10.5, 999.99
    """
    return models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(Decimal("0"))], **kwargs
    )


def make_optional_positive_percentage_decimal_field(**kwargs):
    """
    DecimalField with
    - 5 digits, including 2 decimals
    - min: 0
    - max: 100.00 ()
    - examples: None, 0, 10.5, 99.99, 100
    """
    return models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal("0")), MaxValueValidator(Decimal("100"))],
        **kwargs,
    )


def sum_int_with_potential_null(values_to_sum):
    if all(value is None for value in values_to_sum):
        return 0
    else:
        return sum(value for value in values_to_sum if value is not None)


def read_csv(filepath, delimiter=","):
    with open(filepath, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        return list(reader)


def read_json(filepath):
    with open(filepath) as jsonfile:
        return json.load(jsonfile)
