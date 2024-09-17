import datetime
from decimal import Decimal

from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from data.factories import CanteenFactory, WasteMeasurementFactory
from data.models import Canteen, WasteMeasurement

from .utils import authenticate


class TestWasteMeasurementsApi(APITestCase):
    def test_unauthenticated_create_waste_measurement_call(self):
        """
        When calling this API unathenticated we expect a 403
        """
        canteen = CanteenFactory.create()
        response = self.client.post(reverse("canteen_waste_measurements", kwargs={"canteen_pk": canteen.id}), {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_waste_measurement_missing_canteen(self):
        """
        When calling this API on an unexistent canteen we expect a 404
        """
        self.assertIsNone(Canteen.objects.filter(id=999).first())
        response = self.client.post(
            reverse("canteen_waste_measurements", kwargs={"canteen_pk": 999}),
            {
                "period_start_date": "2024-08-01",
                "period_end_date": "2024-08-10",
                "meal_count": 500,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_waste_measurement_forbidden_canteen(self):
        """
        When calling this API on a canteen that the user doesn't manage,
        we expect a 403
        """
        canteen = CanteenFactory.create()
        response = self.client.post(
            reverse("canteen_waste_measurements", kwargs={"canteen_pk": canteen.id}),
            {
                "period_start_date": "2024-08-01",
                "period_end_date": "2024-08-10",
                "meal_count": 500,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_create_waste_measurement(self):
        """
        When calling this API on a canteen that the user manages
        we expect a waste_measurement to be created
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)

        payload = {
            "period_start_date": "2024-08-01",
            "period_end_date": "2024-08-10",
            "meal_count": 500,
            "total_mass": 100,
            "is_sorted_by_source": True,
            "preparation_total_mass": 20,
            "preparation_is_sorted": True,
            "preparation_edible_mass": 15,
            "preparation_inedible_mass": 5,
            "unserved_total_mass": 50,
            "unserved_is_sorted": False,
            "unserved_edible_mass": "",
            "unserved_inedible_mass": "",
            "leftovers_total_mass": 30.3,
        }

        response = self.client.post(reverse("canteen_waste_measurements", kwargs={"canteen_pk": canteen.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        waste_measurement = WasteMeasurement.objects.get(canteen__id=canteen.id)

        self.assertEqual(waste_measurement.period_start_date, datetime.date(2024, 8, 1))
        self.assertEqual(waste_measurement.period_end_date, datetime.date(2024, 8, 10))
        self.assertEqual(waste_measurement.meal_count, 500)
        self.assertEqual(waste_measurement.total_mass, 100)
        self.assertEqual(waste_measurement.is_sorted_by_source, True)
        self.assertEqual(waste_measurement.preparation_total_mass, 20)
        self.assertEqual(waste_measurement.preparation_is_sorted, True)
        self.assertEqual(waste_measurement.preparation_edible_mass, 15)
        self.assertEqual(waste_measurement.preparation_inedible_mass, 5)
        self.assertEqual(waste_measurement.unserved_total_mass, 50)
        self.assertEqual(waste_measurement.unserved_is_sorted, False)
        self.assertEqual(waste_measurement.unserved_edible_mass, None)
        self.assertEqual(waste_measurement.unserved_inedible_mass, None)
        self.assertEqual(waste_measurement.leftovers_total_mass, Decimal("30.3"))
        self.assertEqual(waste_measurement.leftovers_is_sorted, None)
        self.assertEqual(waste_measurement.leftovers_edible_mass, None)
        self.assertEqual(waste_measurement.leftovers_inedible_mass, None)

    @authenticate
    def test_cannot_create_measurement_without_dates(self):
        """
        Period start date and period end date must be given
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)

        payload = {}

        response = self.client.post(reverse("canteen_waste_measurements", kwargs={"canteen_pk": canteen.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        body = response.json()
        self.assertEqual(body["periodStartDate"][0], "Ce champ est obligatoire.")
        self.assertEqual(body["periodEndDate"][0], "Ce champ est obligatoire.")

    @authenticate
    @freeze_time("2024-08-10")
    def test_cannot_create_future_measurement(self):
        """
        The period end date cannot be in the future
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)

        payload = {
            "period_start_date": "2024-08-01",
            "period_end_date": "2024-08-20",
        }

        response = self.client.post(reverse("canteen_waste_measurements", kwargs={"canteen_pk": canteen.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(response.json()["periodEndDate"][0], "La date doit être dans le passé")

    @authenticate
    def test_start_date_must_be_before_end_date(self):
        """
        The period start date must be before end date
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)

        payload = {
            "period_start_date": "2024-08-10",
            "period_end_date": "2024-08-01",
        }

        response = self.client.post(reverse("canteen_waste_measurements", kwargs={"canteen_pk": canteen.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(response.json()["periodStartDate"][0], "La date de début doit être avant la date de fin")

    @authenticate
    def test_periods_cannot_overlap(self):
        """
        A new measurement cannot have a period that overlaps with an existing measurement
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        WasteMeasurementFactory.create(
            canteen=canteen, period_start_date=datetime.date(2024, 7, 1), period_end_date=datetime.date(2024, 7, 5)
        )

        # check a start date that falls in existing period
        payload = {
            "period_start_date": "2024-07-03",
            "period_end_date": "2024-08-01",
        }
        response = self.client.post(reverse("canteen_waste_measurements", kwargs={"canteen_pk": canteen.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["periodStartDate"][0],
            "Il existe déjà une autre évaluation pour la période 2024-07-01 à 2024-07-05. Veuillez modifier la évaluation existante ou corriger la date de début.",
        )

        # check an end date that falls in existing period
        payload = {
            "period_start_date": "2024-06-10",
            "period_end_date": "2024-07-03",
        }
        response = self.client.post(reverse("canteen_waste_measurements", kwargs={"canteen_pk": canteen.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["periodEndDate"][0],
            "Il existe déjà une autre évaluation pour la période 2024-07-01 à 2024-07-05. Veuillez modifier la évaluation existante ou corriger la date de fin.",
        )

        # check a start and end date that encapsulate the periods of existing measurements
        WasteMeasurementFactory.create(
            canteen=canteen, period_start_date=datetime.date(2024, 7, 10), period_end_date=datetime.date(2024, 7, 15)
        )
        payload = {
            "period_start_date": "2024-06-30",
            "period_end_date": "2024-07-16",
        }
        response = self.client.post(reverse("canteen_waste_measurements", kwargs={"canteen_pk": canteen.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["_All__"][0],
            "Il existe déjà 2 autres évaluations dans la période 2024-06-30 à 2024-07-16. Veuillez modifier les évaluations existantes ou corriger les dates de la période.",
        )

    @authenticate
    def test_ignore_other_canteens_when_validating(self):
        """
        It shouldn't matter when other canteens have created their waste measurements
        """
        WasteMeasurementFactory.create(
            period_start_date=datetime.date(2024, 7, 1), period_end_date=datetime.date(2024, 7, 5)
        )
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)

        response = self.client.post(
            reverse("canteen_waste_measurements", kwargs={"canteen_pk": canteen.id}),
            {
                "period_start_date": "2024-07-01",
                "period_end_date": "2024-07-05",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unauthenticated_get_waste_measurements(self):
        """
        Get 403 when trying to fetch waste measurements without being authenticated
        """
        canteen = CanteenFactory.create()
        response = self.client.get(reverse("canteen_waste_measurements", kwargs={"canteen_pk": canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_get_waste_measurements_forbidden_canteen(self):
        """
        Get 403 when trying to fetch waste measurements without being manager of the canteen
        """
        canteen = CanteenFactory.create()
        response = self.client.get(reverse("canteen_waste_measurements", kwargs={"canteen_pk": canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_get_waste_measurements(self):
        """
        Canteen managers can fetch all the waste measurements for a canteen in order of period start date descending
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        measurement_july = WasteMeasurementFactory.create(
            canteen=canteen, period_start_date=datetime.date(2024, 7, 1), period_end_date=datetime.date(2024, 7, 5)
        )
        measurement_august = WasteMeasurementFactory.create(
            canteen=canteen, period_start_date=datetime.date(2024, 8, 1), period_end_date=datetime.date(2024, 8, 5)
        )
        WasteMeasurementFactory.create()  # to be filtered out

        response = self.client.get(reverse("canteen_waste_measurements", kwargs={"canteen_pk": canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()

        self.assertEqual(len(body), 2)
        self.assertEqual(body[0]["id"], measurement_august.id)
        self.assertEqual(body[1]["id"], measurement_july.id)

    @authenticate
    def test_get_period_day_count(self):
        """
        Canteen waste measurements should contain a computed field of number of days in period
        """
        measurement = WasteMeasurementFactory.create(
            period_start_date=datetime.date(2024, 8, 1), period_end_date=datetime.date(2024, 8, 5)
        )
        canteen = measurement.canteen
        canteen.managers.add(authenticate.user)

        response = self.client.get(reverse("canteen_waste_measurements", kwargs={"canteen_pk": canteen.id}))
        body = response.json()

        self.assertEqual(body[0]["daysInPeriod"], 5)

    @authenticate
    def test_get_estimated_total_waste_for_year(self):
        """
        Canteen waste measurements should contain a computed field of total waste for the year in kg
        This is done by taking dividing the total mass by period meal count and multiplying by canteen's
        yearly meal count
        """
        canteen = CanteenFactory(yearly_meal_count=1000)
        canteen.managers.add(authenticate.user)
        WasteMeasurementFactory.create(canteen=canteen, meal_count=10, total_mass=50)

        response = self.client.get(reverse("canteen_waste_measurements", kwargs={"canteen_pk": canteen.id}))
        body = response.json()

        self.assertEqual(body[0]["totalYearlyWasteEstimation"], 5000)

    @authenticate
    def test_cannot_get_waste_measurement_not_manager(self):
        """
        If the user is not the manager of the canteen, they get a 403 when attempting to view the waste measurement
        """
        canteen = CanteenFactory.create()
        measurement = WasteMeasurementFactory.create(canteen=canteen)

        response = self.client.get(
            reverse("canteen_waste_measurement", kwargs={"pk": measurement.id, "canteen_pk": canteen.id})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_get_waste_measurement(self):
        """
        Canteen managers can fetch the waste measurement of a canteen they manage
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        measurement = WasteMeasurementFactory.create(canteen=canteen)

        response = self.client.get(
            reverse("canteen_waste_measurement", kwargs={"pk": measurement.id, "canteen_pk": canteen.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertIn("periodStartDate", body)

    @authenticate
    def test_update_waste_measurement(self):
        """
        Canteen managers can edit the waste measurement of a canteen they manage
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        measurement = WasteMeasurementFactory.create(canteen=canteen, meal_count=100)

        payload = {"mealCount": 200}
        response = self.client.patch(
            reverse("canteen_waste_measurement", kwargs={"pk": measurement.id, "canteen_pk": canteen.id}), payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(body["mealCount"], 200)

    @authenticate
    @freeze_time("2024-08-10")
    def test_cannot_update_date_to_future(self):
        """
        The period end date cannot be updated to be in the future
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        measurement = WasteMeasurementFactory.create(
            canteen=canteen, period_start_date="2024-08-01", period_end_date="2024-08-05"
        )

        payload = {"period_end_date": "2024-08-20"}
        response = self.client.patch(
            reverse("canteen_waste_measurement", kwargs={"pk": measurement.id, "canteen_pk": canteen.id}), payload
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(response.json()["periodEndDate"][0], "La date doit être dans le passé")

    @authenticate
    def test_start_date_must_be_before_end_date_in_update(self):
        """
        The period start date must be before end date in update
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        measurement = WasteMeasurementFactory.create(
            canteen=canteen, period_start_date=datetime.date(2024, 8, 1), period_end_date=datetime.date(2024, 8, 5)
        )

        payload = {"period_start_date": "2024-08-10"}
        response = self.client.patch(
            reverse("canteen_waste_measurement", kwargs={"pk": measurement.id, "canteen_pk": canteen.id}), payload
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["periodStartDate"][0], "La date de début doit être avant la date de fin")

        payload = {"period_end_date": "2024-08-1"}
        response = self.client.patch(
            reverse("canteen_waste_measurement", kwargs={"pk": measurement.id, "canteen_pk": canteen.id}), payload
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["periodEndDate"][0], "La date de fin doit être après la date de début")

    @authenticate
    def test_periods_cannot_overlap_in_update(self):
        """
        A measurement update cannot have a period that overlaps with an existing measurement
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        WasteMeasurementFactory.create(
            canteen=canteen, period_start_date=datetime.date(2024, 7, 1), period_end_date=datetime.date(2024, 7, 5)
        )
        measurement = WasteMeasurementFactory.create(
            canteen=canteen, period_start_date=datetime.date(2024, 8, 1), period_end_date=datetime.date(2024, 8, 5)
        )

        # check a start date that falls in existing period
        payload = {"period_start_date": "2024-07-03"}
        response = self.client.patch(
            reverse("canteen_waste_measurement", kwargs={"pk": measurement.id, "canteen_pk": canteen.id}), payload
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["periodStartDate"][0],
            "Il existe déjà une autre évaluation pour la période 2024-07-01 à 2024-07-05. Veuillez modifier la évaluation existante ou corriger la date de début.",
        )

        # check an end date that falls in existing period
        measurement = WasteMeasurementFactory.create(
            canteen=canteen, period_start_date=datetime.date(2024, 6, 1), period_end_date=datetime.date(2024, 6, 5)
        )
        payload = {"period_end_date": "2024-07-03"}
        response = self.client.patch(
            reverse("canteen_waste_measurement", kwargs={"pk": measurement.id, "canteen_pk": canteen.id}), payload
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["periodEndDate"][0],
            "Il existe déjà une autre évaluation pour la période 2024-07-01 à 2024-07-05. Veuillez modifier la évaluation existante ou corriger la date de fin.",
        )

        # check a start and end date that encapsulate the periods of existing measurements
        payload = {
            "period_start_date": "2024-01-30",
            "period_end_date": "2024-08-10",
        }
        response = self.client.patch(
            reverse("canteen_waste_measurement", kwargs={"pk": measurement.id, "canteen_pk": canteen.id}), payload
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["_All__"][0],
            "Il existe déjà 2 autres évaluations dans la période 2024-01-30 à 2024-08-10. Veuillez modifier les évaluations existantes ou corriger les dates de la période.",
        )

    @authenticate
    def test_cannot_delete_dates(self):
        """
        The period dates cannot be removed
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        measurement = WasteMeasurementFactory.create(canteen=canteen)

        payload = {
            "period_start_date": None,
            "period_end_date": "",
        }
        response = self.client.patch(
            reverse("canteen_waste_measurement", kwargs={"pk": measurement.id, "canteen_pk": canteen.id}),
            payload,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(response.json()["periodStartDate"][0], "Ce champ ne peut être nul.")
        self.assertEqual(
            response.json()["periodEndDate"][0],
            "La date n'a pas le bon format. Utilisez un des formats suivants\xa0: YYYY-MM-DD.",
        )

    @authenticate
    def test_can_update_period(self):
        """
        Given valid dates, it it possible to update the dates of a measurement even when the new dates "overlap" the existing ones
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        measurement = WasteMeasurementFactory.create(
            canteen=canteen, period_start_date=datetime.date(2024, 5, 1), period_end_date=datetime.date(2024, 5, 10)
        )

        payload = {"period_start_date": "2024-04-01", "period_end_date": "2024-07-01"}
        response = self.client.patch(
            reverse("canteen_waste_measurement", kwargs={"pk": measurement.id, "canteen_pk": canteen.id}), payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        measurement.refresh_from_db()
        self.assertEqual(measurement.period_start_date, datetime.date(2024, 4, 1))
        self.assertEqual(measurement.period_end_date, datetime.date(2024, 7, 1))
