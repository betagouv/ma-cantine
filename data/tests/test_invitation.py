from django.core.exceptions import ValidationError
from django.test import TestCase

from data.factories import CanteenFactory, InvitationFactory
from data.models import Canteen, Invitation


class InvitationModelSaveTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen_groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        cls.canteen_groupe_2 = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        cls.canteen_satellite = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL)
        cls.canteen_site = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE)

    def test_invitation_add_satellite_ok(self):
        for invited_canteen in [self.canteen_satellite, self.canteen_site]:
            with self.subTest(invited_canteen=invited_canteen):
                invitation = InvitationFactory(creation_canteen=self.canteen_groupe, invited_canteen=invited_canteen)
                self.assertEqual(invitation.status, Invitation.Status.SENT)

    def test_invitation_creation_canteen_validation(self):
        for creation_canteen in [self.canteen_satellite, self.canteen_site]:
            with self.subTest(creation_canteen=creation_canteen):
                with self.assertRaises(ValidationError) as context:
                    InvitationFactory(creation_canteen=creation_canteen)
                self.assertIn(
                    "Le champ doit être une cantine de type 'Groupe'.",
                    context.exception.message_dict["creation_canteen"],
                )

    def test_invitation_invited_canteen_empty(self):
        with self.assertRaises(ValidationError) as context:
            InvitationFactory(creation_canteen=self.canteen_groupe, invited_canteen=None)
        self.assertIn("Le champ ne peut pas être vide.", context.exception.message_dict["invited_canteen"])

    def test_invitation_invited_canteen_cannot_be_groupe(self):
        with self.assertRaises(ValidationError) as context:
            InvitationFactory(creation_canteen=self.canteen_groupe, invited_canteen=self.canteen_groupe_2)
        self.assertIn(
            "Le champ ne peut pas être une cantine de type 'Groupe'.",
            context.exception.message_dict["invited_canteen"],
        )

    def test_invitation_invited_canteen_already_in_groupe(self):
        canteen_satellite_in_groupe = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=self.canteen_groupe_2
        )
        with self.assertRaises(ValidationError) as context:
            InvitationFactory(creation_canteen=self.canteen_groupe, invited_canteen=canteen_satellite_in_groupe)
        self.assertIn(
            "Cette cantine est déjà rattachée à un groupe.", context.exception.message_dict["invited_canteen"]
        )

    def test_invitation_invited_canteen_already_has_pending_invitation(self):
        InvitationFactory(creation_canteen=self.canteen_groupe, invited_canteen=self.canteen_satellite)
        # same groupe
        with self.assertRaises(ValidationError) as context:
            InvitationFactory(creation_canteen=self.canteen_groupe, invited_canteen=self.canteen_satellite)
        self.assertIn(
            "Cette cantine a déjà une invitation en attente de ce groupe.",
            context.exception.message_dict["invited_canteen"],
        )
        # other groupe
        with self.assertRaises(ValidationError) as context:
            InvitationFactory(creation_canteen=self.canteen_groupe_2, invited_canteen=self.canteen_satellite)
        self.assertIn(
            "Cette cantine a déjà une invitation en attente d'un autre groupe.",
            context.exception.message_dict["invited_canteen"],
        )

    def test_invitation_invited_canteen_with_answered_invitations(self):
        for status in [Invitation.Status.ACCEPTED, Invitation.Status.DECLINED, Invitation.Status.CANCELLED]:
            InvitationFactory(creation_canteen=self.canteen_groupe, invited_canteen=self.canteen_site, status=status)
        invitation = InvitationFactory(creation_canteen=self.canteen_groupe, invited_canteen=self.canteen_site)
        self.assertEqual(invitation.status, Invitation.Status.SENT)

    def test_invitation_pending_can_be_saved_again(self):
        invitation = InvitationFactory(creation_canteen=self.canteen_groupe, invited_canteen=self.canteen_satellite)
        invitation.save()

    def test_invitation_accepted_can_be_saved_once_canteen_in_groupe(self):
        invitation = InvitationFactory(creation_canteen=self.canteen_groupe, invited_canteen=self.canteen_satellite)
        self.canteen_satellite.groupe = self.canteen_groupe
        self.canteen_satellite.save()
        invitation.status = Invitation.Status.ACCEPTED
        invitation.save()
