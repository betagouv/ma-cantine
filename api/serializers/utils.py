from rest_framework import serializers


class PurchaseField(serializers.DecimalField):
    def __init__(self):
        super().__init__(max_digits=20, decimal_places=2, required=False)


def choice_list_to_choices(choice_list):
    return [(choice.value, choice.label) for choice in choice_list]
