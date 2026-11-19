import importlib

from django.apps import apps
from django.test import TestCase

from data.factories import PartnerFactory
from data.models import Partner, PartnerType, PartnerTypeM2M

migration = importlib.import_module("data.migrations.0309_partner_type_list")


class PartnerTypeListMigrationTest(TestCase):
    def test_populate_type_list_from_types(self):
        entreprise = PartnerTypeM2M.objects.create(name="Entreprise privée")
        logiciel = PartnerTypeM2M.objects.create(name="Logiciels / outils numériques")
        partner_with_types = PartnerFactory()
        partner_with_types.types.add(entreprise, logiciel)
        partner_without_types = PartnerFactory()

        migration.populate_type_list_from_types(apps, None)

        # enum order, not M2M order
        self.assertEqual(
            Partner.objects.get(id=partner_with_types.id).type_list,
            [PartnerType.LOGICIEL, PartnerType.ENTREPRISE_PRIVEE],
        )
        self.assertEqual(Partner.objects.get(id=partner_without_types.id).type_list, [])

    def test_all_enum_values_are_mapped(self):
        self.assertEqual(
            {(value, name) for name, value in migration.PARTNER_TYPE_VALUE_FROM_NAME.items()}, set(PartnerType.choices)
        )

    def test_unknown_name_fails(self):
        partner = PartnerFactory()
        partner.types.add(PartnerTypeM2M.objects.create(name="Type inconnu"))

        with self.assertRaises(KeyError):
            migration.populate_type_list_from_types(apps, None)
