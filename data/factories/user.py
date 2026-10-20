import factory
from django.contrib.auth import get_user_model


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Sequence(lambda n: f"user_{n}@example.net")
    is_dev = False

    @classmethod
    def _create(cls, model_class, *args, skip_validations=False, **kwargs):
        """
        skip_validations=True: to create a user that doesn't pass the validations (e.g. missing or invalid data)
        Usage: UserFactory(email="invalid", skip_validations=True)
        """
        obj = model_class(*args, **kwargs)
        obj.save(skip_validations=skip_validations)
        return obj
