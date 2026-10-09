from rest_framework import serializers


class PurchaseField(serializers.DecimalField):
    def __init__(self):
        super().__init__(max_digits=20, decimal_places=2, required=False)


# Set all the serializer fields as read_only (declared fields & ModelSerializer generated fields)
# Usage: class MySerializer(ReadOnlySerializerMixin, serializers.ModelSerializer)
# (comment instead of docstring: drf-spectacular would use it as the description of every serializer)
class ReadOnlySerializerMixin:
    def get_extra_kwargs(self):
        # ModelSerializer only: build the generated fields as read_only (like Meta.read_only_fields)
        extra_kwargs = super().get_extra_kwargs()
        fields = getattr(self.Meta, "fields", None)
        if isinstance(fields, (list, tuple)):
            for field_name in fields:
                extra_kwargs.setdefault(field_name, {})["read_only"] = True
        return extra_kwargs

    def get_fields(self):
        # declared fields (& ModelSerializer generated fields if Meta.fields = "__all__")
        fields = super().get_fields()
        for field in fields.values():
            field.read_only = True
            field.required = False  # read_only fields can't be required
        return fields


def choice_list_to_choices(choice_list):
    return [(choice.value, choice.label) for choice in choice_list]


def set_help_text_from_verbose_name(serializer_class):
    """
    Set help_text for serializer fields based on model field verbose_name
    """
    if hasattr(serializer_class, "Meta") and hasattr(serializer_class.Meta, "model"):
        model = serializer_class.Meta.model

        # Override get_fields to set help_text
        original_get_fields = getattr(serializer_class, "get_fields")

        def get_fields(self):
            fields = original_get_fields(self)  # Call original method

            # Set help_text for model fields
            for field_name, field in fields.items():
                try:
                    model_field = model._meta.get_field(field_name)
                    if hasattr(model_field, "verbose_name") and model_field.verbose_name:
                        field.help_text = model_field.verbose_name
                except Exception:
                    # Field might not exist in model (computed properties, etc.)
                    pass

            return fields

        # Replace the method
        setattr(serializer_class, "get_fields", get_fields)

        return serializer_class

    return serializer_class
