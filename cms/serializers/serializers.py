from rest_framework import serializers


class ChoiceField(serializers.ChoiceField):
    def to_representation(self, obj):
        if obj == "" and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        # To support inserts with the value
        if data == "" and self.allow_blank:
            return ""

        for key, val in self._choices.items():
            if val == data:
                return key


class ChoiceArrayField(serializers.Field):
    def __init__(self, choices=None, **kwargs):
        self.choices = dict(choices) if choices else {}
        super().__init__(**kwargs)

    def to_representation(self, value):
        if value is None:
            return []
        return [self.choices.get(item, item) for item in value]

    def to_internal_value(self, data):
        if data is None:
            return []
        return [key for key, val in self.choices.items() if val in data]
