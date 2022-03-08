import factory.random
from random import randint
from django.conf import settings
from django.test.runner import DiscoverRunner


class MaCantineTestRunner(DiscoverRunner):
    def setup_test_environment(self, **kwargs):
        override_seed = settings.OVERRIDE_TEST_SEED
        seed = int(override_seed) if override_seed else randint(0, 65535)
        factory.random.reseed_random(seed)
        print("Using seed: {}".format(seed))
        super().setup_test_environment(**kwargs)
