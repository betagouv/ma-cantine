from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time

from common.tests.utils import date_in_campaign

from data.factories import CanteenFactory, DiagnosticFactory, InvitationFactory, UserFactory
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

    def test_invitation_invited_canteen_must_be_satellite_or_site(self):
        # CENTRAL & CENTRAL_SERVING are no longer allowed on save (legacy data only)
        canteen_central = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE)
        Canteen.objects.filter(id=canteen_central.id).update(production_type=Canteen.ProductionType.CENTRAL)
        canteen_central.refresh_from_db()
        for invited_canteen in [self.canteen_groupe_2, canteen_central]:
            with self.subTest(invited_canteen=invited_canteen):
                with self.assertRaises(ValidationError) as context:
                    InvitationFactory(creation_canteen=self.canteen_groupe, invited_canteen=invited_canteen)
                self.assertIn(
                    "Le champ doit être un restaurant satellite ou un restaurant avec cuisine sur place.",
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
            InvitationFactory(
                creation_canteen=self.canteen_groupe,
                invited_canteen=self.canteen_site,
                status=status,
                answer_date=timezone.now(),
            )
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
        invitation.answer_date = timezone.now()
        invitation.save()

    def test_invitation_pending_answer_fields_must_be_empty(self):
        user = UserFactory()
        for field_name, value in [("answer_user", user), ("answer_date", timezone.now())]:
            with self.subTest(field_name=field_name):
                with self.assertRaises(ValidationError) as context:
                    InvitationFactory(creation_canteen=self.canteen_groupe, **{field_name: value})
                self.assertIn(
                    "Le champ doit être vide tant que l'invitation est en attente.",
                    context.exception.message_dict[field_name],
                )

    def test_invitation_answered_answer_date_must_be_filled(self):
        for status in [Invitation.Status.ACCEPTED, Invitation.Status.DECLINED, Invitation.Status.CANCELLED]:
            with self.subTest(status=status):
                with self.assertRaises(ValidationError) as context:
                    InvitationFactory(creation_canteen=self.canteen_groupe, status=status)
                self.assertIn(
                    "Le champ doit être rempli une fois que l'invitation a reçu une réponse.",
                    context.exception.message_dict["answer_date"],
                )

    def test_invitation_answered_answer_user_can_be_empty(self):
        invitation = InvitationFactory(
            creation_canteen=self.canteen_groupe,
            status=Invitation.Status.DECLINED,
            answer_date=timezone.now(),
            answer_user=None,
        )
        self.assertIsNone(invitation.answer_user)


class InvitationModelAnswerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.canteen_groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        cls.canteen_groupe_2 = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        cls.canteen_satellite = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL)

    def setUp(self):
        self.invitation = InvitationFactory(
            creation_canteen=self.canteen_groupe, invited_canteen=self.canteen_satellite
        )
        self.invitation_declined = InvitationFactory(
            creation_canteen=self.canteen_groupe, status=Invitation.Status.DECLINED, answer_date=timezone.now()
        )

    def test_accept(self):
        self.invitation.accept(self.user)
        self.assertEqual(self.invitation.status, Invitation.Status.ACCEPTED)
        self.assertEqual(self.invitation.answer_user, self.user)
        self.assertIsNotNone(self.invitation.answer_date)
        self.canteen_satellite.refresh_from_db()
        self.assertEqual(self.canteen_satellite.groupe, self.canteen_groupe)

    def test_cannot_accept_if_not_pending(self):
        with self.assertRaises(ValidationError) as context:
            self.invitation_declined.accept(self.user)
        self.assertIn("L'invitation n'est plus en attente.", context.exception.message_dict["status"])
        self.invitation_declined.refresh_from_db()
        self.assertEqual(self.invitation_declined.status, Invitation.Status.DECLINED)
        self.assertIsNone(self.invitation_declined.invited_canteen.groupe)

    def test_cannot_accept_if_canteen_linked_to_a_groupe_since(self):
        self.canteen_satellite.groupe = self.canteen_groupe_2
        self.canteen_satellite.save()
        with self.assertRaises(ValidationError) as context:
            self.invitation.accept(self.user)
        self.assertIn(
            "Cette cantine est déjà rattachée à un groupe.", context.exception.message_dict["invited_canteen"]
        )
        self.invitation.refresh_from_db()
        self.assertEqual(self.invitation.status, Invitation.Status.SENT)
        self.canteen_satellite.refresh_from_db()
        self.assertEqual(self.canteen_satellite.groupe, self.canteen_groupe_2)

    @freeze_time(date_in_campaign(2024))
    def test_cannot_accept_during_teledeclaration_if_groupe_has_diagnostic_teledeclared(self):
        # a groupe needs a manager & at least 1 satellite to teledeclare
        self.canteen_groupe.managers.add(self.user)
        CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=self.canteen_groupe)
        DiagnosticFactory(canteen=self.canteen_groupe, year=2024, valeur_totale=100).teledeclare(applicant=self.user)
        with self.assertRaises(ValidationError) as context:
            self.invitation.accept(self.user)
        self.assertIn("groupe", context.exception.message_dict)
        self.invitation.refresh_from_db()
        self.assertEqual(self.invitation.status, Invitation.Status.SENT)
        self.canteen_satellite.refresh_from_db()
        self.assertIsNone(self.canteen_satellite.groupe)


class InvitationQuerySetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.canteen_groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE, managers=[cls.user])
        cls.canteen_groupe_other = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        cls.canteen_satellite = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, managers=[cls.user]
        )
        cls.canteen_satellite_other = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL)
        cls.canteen_satellite_other_2 = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL)
        cls.invitation_sent = InvitationFactory(
            creation_canteen=cls.canteen_groupe, invited_canteen=cls.canteen_satellite_other
        )
        cls.invitation_received = InvitationFactory(
            creation_canteen=cls.canteen_groupe_other, invited_canteen=cls.canteen_satellite
        )
        cls.invitation_other = InvitationFactory(
            creation_canteen=cls.canteen_groupe_other, invited_canteen=cls.canteen_satellite_other_2
        )

    def test_for_user(self):
        self.assertEqual(set(Invitation.objects.for_user(self.user)), {self.invitation_sent, self.invitation_received})
        self.assertEqual(Invitation.objects.for_user(UserFactory()).count(), 0)

    def test_annotate_with_direction(self):
        invitations = Invitation.objects.for_user(self.user).annotate_with_direction(self.user)
        self.assertEqual(invitations.get(id=self.invitation_sent.id).direction, Invitation.Direction.SENT)
        self.assertEqual(invitations.get(id=self.invitation_received.id).direction, Invitation.Direction.RECEIVED)

    def test_annotate_with_direction_user_manages_both_canteens(self):
        self.canteen_groupe_other.managers.add(self.user)
        invitation = Invitation.objects.annotate_with_direction(self.user).get(id=self.invitation_received.id)
        self.assertEqual(invitation.direction, Invitation.Direction.RECEIVED)
