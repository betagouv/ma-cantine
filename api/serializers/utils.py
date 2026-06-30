from rest_framework import serializers


class PurchaseField(serializers.DecimalField):
    def __init__(self):
        super().__init__(max_digits=20, decimal_places=2, required=False)


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
