import datetime
from decimal import Decimal

from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import authenticate, get_oauth2_token
from data.factories import CanteenFactory, WasteMeasurementFactory
from data.models import WasteMeasurement


class WasteMeasurementsListApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory(yearly_meal_count=1000)

    def test_cannot_get_waste_measurements_if_unauthenticated(self):
        response = self.client.get(reverse("canteen_waste_measurements_list", kwargs={"canteen_pk": self.canteen.id}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_get_waste_measurements_if_canteen_unknown(self):
        response = self.client.get(reverse("canteen_waste_measurements_list", kwargs={"canteen_pk": 9909}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_cannot_get_waste_measurements_if_not_canteen_manager(self):
        response = self.client.get(reverse("canteen_waste_measurements_list", kwargs={"canteen_pk": self.canteen.id}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_get_waste_measurements(self):
        self.canteen.managers.add(authenticate.user)
        measurement_july = WasteMeasurementFactory(
            canteen=self.canteen,
            period_start_date=datetime.date(2024, 7, 1),
            period_end_date=datetime.date(2024, 7, 5),
        )
        measurement_august = WasteMeasurementFactory(
            canteen=self.canteen,
            period_start_date=datetime.date(2024, 8, 1),
            period_end_date=datetime.date(2024, 8, 5),
        )
        WasteMeasurementFactory()  # will not be returned

        response = self.client.get(reverse("canteen_waste_measurements_list", kwargs={"canteen_pk": self.canteen.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body), 2)
        self.assertEqual(body[0]["id"], measurement_august.id)  # ordered by period_start_date desc
        self.assertEqual(body[1]["id"], measurement_july.id)

    def test_get_waste_measurements_via_oauth2(self):
        """
        Canteen managers can fetch all the waste measurements for a canteen they manage via oauth2 token
        """
        user, token = get_oauth2_token("waste_measurements:read")
        self.canteen.managers.add(user)
        measurement_july = WasteMeasurementFactory(
            canteen=self.canteen,
            period_start_date=datetime.date(2024, 7, 1),
            period_end_date=datetime.date(2024, 7, 5),
        )
        measurement_august = WasteMeasurementFactory(
            canteen=self.canteen,
            period_start_date=datetime.date(2024, 8, 1),
            period_end_date=datetime.date(2024, 8, 5),
        )
        WasteMeasurementFactory()  # will not be returned

        self.client.credentials(Authorization=f"Bearer {token}")
        response = self.client.get(reverse("canteen_waste_measurements_list", kwargs={"canteen_pk": self.canteen.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body), 2)
        self.assertEqual(body[0]["id"], measurement_august.id)  # ordered by period_start_date desc
        self.assertEqual(body[1]["id"], measurement_july.id)

    @authenticate
    def test_get_period_day_count(self):
        self.canteen.managers.add(authenticate.user)
        WasteMeasurementFactory(
            canteen=self.canteen,
            period_start_date=datetime.date(2024, 8, 1),
            period_end_date=datetime.date(2024, 8, 5),
        )

        response = self.client.get(reverse("canteen_waste_measurements_list", kwargs={"canteen_pk": self.canteen.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body[0]["daysInPeriod"], 5)

    @authenticate
    def test_get_estimated_total_waste_for_year(self):
        """
        Canteen waste measurements should contain a computed field of total waste for the year in kg
        This is done by taking dividing the total mass by period meal count and multiplying by canteen's
        yearly meal count
        """
        self.canteen.managers.add(authenticate.user)
        WasteMeasurementFactory(canteen=self.canteen, meal_count=10, total_mass=50)

        response = self.client.get(reverse("canteen_waste_measurements_list", kwargs={"canteen_pk": self.canteen.id}))

        body = response.json()
        self.assertEqual(body[0]["totalYearlyWasteEstimation"], 5000)

    @authenticate
    def test_get_waste_measurements_for_period(self):
        """
        Canteen managers can fetch all the waste measurements for a canteen in a particular time period
        """
        self.canteen.managers.add(authenticate.user)
        measurement_july = WasteMeasurementFactory(
            canteen=self.canteen,
            period_start_date=datetime.date(2024, 7, 1),
            period_end_date=datetime.date(2024, 7, 5),
        )
        measurement_august = WasteMeasurementFactory(
            canteen=self.canteen,
            period_start_date=datetime.date(2024, 8, 1),
            period_end_date=datetime.date(2024, 8, 5),
        )
        # the following should be filtered out
        WasteMeasurementFactory(
            canteen=self.canteen,
            period_start_date=datetime.date(2024, 9, 1),
            period_end_date=datetime.date(2024, 9, 5),
        )

        query = "?period_start_date_after=2024-07-01&period_end_date_before=2024-09-01"
        path = reverse("canteen_waste_measurements_list", kwargs={"canteen_pk": self.canteen.id})
        response = self.client.get(path + query)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body), 2)
        self.assertEqual(body[0]["id"], measurement_august.id)
        self.assertEqual(body[1]["id"], measurement_july.id)


class WasteMeasurementsCreateApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        cls.url = reverse("canteen_waste_measurements_list", kwargs={"canteen_pk": cls.canteen.id})

    def test_cannot_create_waste_measurement_if_unauthenticated(self):
        response = self.client.post(self.url, {})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_create_waste_measurement_if_canteen_unknown(self):
        response = self.client.post(
            reverse("canteen_waste_measurements_list", kwargs={"canteen_pk": 9999}),
            {
                "period_start_date": "2024-08-01",
                "period_end_date": "2024-08-10",
                "meal_count": 500,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_cannot_create_waste_measurement_if_not_canteen_manager(self):
        response = self.client.post(
            self.url,
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
        self.canteen.managers.add(authenticate.user)

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

        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        waste_measurement = WasteMeasurement.objects.get(canteen__id=self.canteen.id)
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

    def test_create_waste_measurement_via_oauth2(self):
        user, token = get_oauth2_token("waste_measurements:create")
        self.canteen.managers.add(user)

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

        self.client.credentials(Authorization=f"Bearer {token}")
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @authenticate
    def test_create_waste_measurement_single_day(self):
        """
        Same start & end dates (Period of 1 day)
        """
        self.canteen.managers.add(authenticate.user)

        payload = {
            "period_start_date": "2024-08-01",
            "period_end_date": "2024-08-01",
        }

        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @authenticate
    def test_cannot_create_measurement_without_dates(self):
        """
        Period start date and period end date must be given
        """
        self.canteen.managers.add(authenticate.user)

        payload = {}

        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        body = response.json()
        self.assertEqual(body["periodStartDate"][0], "Champ requis.")
        self.assertEqual(body["periodEndDate"][0], "Champ requis.")

    @authenticate
    @freeze_time("2024-08-10")
    def test_cannot_create_future_measurement(self):
        """
        The period end date cannot be in the future
        """
        self.canteen.managers.add(authenticate.user)

        payload = {
            "period_start_date": "2024-08-01",
            "period_end_date": "2024-08-20",
        }

        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["periodEndDate"][0], "La date ne peut pas être dans le futur")

    @authenticate
    def test_start_date_must_be_before_end_date(self):
        """
        The period start date must be before end date
        """
        self.canteen.managers.add(authenticate.user)

        payload = {
            "period_start_date": "2024-08-10",
            "period_end_date": "2024-08-01",
        }

        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["periodStartDate"][0], "La date de début ne peut pas être après la date de fin"
        )

    @authenticate
    def test_periods_cannot_overlap(self):
        """
        A new measurement cannot have a period that overlaps with an existing measurement
        """
        self.canteen.managers.add(authenticate.user)
        WasteMeasurementFactory(
            canteen=self.canteen,
            period_start_date=datetime.date(2024, 7, 1),
            period_end_date=datetime.date(2024, 7, 5),
        )

        # check a start date that falls in existing period
        payload = {
            "period_start_date": "2024-07-03",
            "period_end_date": "2024-08-01",
        }

        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["_All__"][0],
            "Il existe déjà une autre évaluation dans la période 2024-07-03 à 2024-08-01. Veuillez modifier l'évaluation existante ou corriger les dates de la période.",
        )

        # check an end date that falls in existing period
        payload = {
            "period_start_date": "2024-06-10",
            "period_end_date": "2024-07-03",
        }

        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["_All__"][0],
            "Il existe déjà une autre évaluation dans la période 2024-06-10 à 2024-07-03. Veuillez modifier l'évaluation existante ou corriger les dates de la période.",
        )

        # check a start and end date that encapsulate the periods of existing measurements
        WasteMeasurementFactory(
            canteen=self.canteen,
            period_start_date=datetime.date(2024, 7, 10),
            period_end_date=datetime.date(2024, 7, 15),
        )
        payload = {
            "period_start_date": "2024-06-30",
            "period_end_date": "2024-07-16",
        }

        response = self.client.post(self.url, payload)

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
        WasteMeasurementFactory(period_start_date=datetime.date(2024, 7, 1), period_end_date=datetime.date(2024, 7, 5))
        self.canteen.managers.add(authenticate.user)

        response = self.client.post(
            self.url,
            {
                "period_start_date": "2024-07-01",
                "period_end_date": "2024-07-05",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class WasteMeasurementsDetailApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        cls.measurement = WasteMeasurementFactory(
            canteen=cls.canteen, period_start_date=datetime.date(2023, 1, 1), period_end_date=datetime.date(2023, 1, 5)
        )
        cls.url = reverse(
            "canteen_waste_measurement_detail", kwargs={"pk": cls.measurement.id, "canteen_pk": cls.canteen.id}
        )

    @authenticate
    def test_cannot_get_waste_measurement_if_unauthenticated(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_get_waste_measurement_if_canteen_unknown(self):
        response = self.client.get(
            reverse("canteen_waste_measurement_detail", kwargs={"pk": self.measurement.id, "canteen_pk": 9909})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_cannot_get_waste_measurement_if_not_canteen_manager(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_get_waste_measurement_if_not_corresponding_canteen(self):
        canteen2 = CanteenFactory()
        measurement2 = WasteMeasurementFactory(
            canteen=canteen2, period_start_date=datetime.date(2023, 1, 1), period_end_date=datetime.date(2023, 1, 5)
        )
        self.canteen.managers.add(authenticate.user)

        response = self.client.get(
            reverse(
                "canteen_waste_measurement_detail",
                kwargs={"pk": measurement2.id, "canteen_pk": self.canteen.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # even if user manages the canteen of the measurement
        canteen2.managers.add(authenticate.user)

        response = self.client.get(
            reverse(
                "canteen_waste_measurement_detail",
                kwargs={"pk": measurement2.id, "canteen_pk": self.canteen.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_get_waste_measurement(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertIn("periodStartDate", body)
        self.assertIn("periodEndDate", body)

    def test_get_waste_measurement_via_oauth2(self):
        user, token = get_oauth2_token("waste_measurements:read")
        self.canteen.managers.add(user)

        self.client.credentials(Authorization=f"Bearer {token}")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertIn("periodStartDate", body)
        self.assertIn("periodEndDate", body)


class WasteMeasurementsUpdateApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        cls.measurement = WasteMeasurementFactory(
            canteen=cls.canteen,
            meal_count=100,
            period_start_date=datetime.date(2023, 1, 1),
            period_end_date=datetime.date(2023, 1, 5),
        )
        cls.url = reverse(
            "canteen_waste_measurement_detail", kwargs={"pk": cls.measurement.id, "canteen_pk": cls.canteen.id}
        )

    @authenticate
    def test_cannot_update_waste_measurement_if_unauthenticated(self):
        payload = {"mealCount": 200}

        response = self.client.patch(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_update_waste_measurement_if_canteen_unknown(self):
        payload = {"mealCount": 200}

        response = self.client.get(
            reverse("canteen_waste_measurement_detail", kwargs={"pk": self.measurement.id, "canteen_pk": 9909}),
            payload,
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_cannot_update_waste_measurement_if_measurement_unknown(self):
        self.canteen.managers.add(authenticate.user)
        payload = {"mealCount": 200}

        response = self.client.get(
            reverse("canteen_waste_measurement_detail", kwargs={"pk": 9999, "canteen_pk": self.canteen.id}), payload
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_cannot_update_waste_measurement_if_not_canteen_manager(self):
        payload = {"mealCount": 200}

        response = self.client.patch(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_update_waste_measurement_if_not_corresponding_canteen(self):
        canteen_other = CanteenFactory()
        measurement_other = WasteMeasurementFactory(
            canteen=canteen_other,
            period_start_date=datetime.date(2023, 1, 1),
            period_end_date=datetime.date(2023, 1, 5),
        )
        self.canteen.managers.add(authenticate.user)
        payload = {"mealCount": 200}

        response = self.client.patch(
            reverse(
                "canteen_waste_measurement_detail",
                kwargs={"pk": measurement_other.id, "canteen_pk": self.canteen.id},
            ),
            payload,
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # even if user manages canteen_other
        canteen_other.managers.add(authenticate.user)

        response = self.client.patch(
            reverse(
                "canteen_waste_measurement_detail",
                kwargs={"pk": measurement_other.id, "canteen_pk": self.canteen.id},
            ),
            payload,
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_update_waste_measurement(self):
        """
        Canteen managers can edit the waste measurement of a canteen they manage
        """
        self.canteen.managers.add(authenticate.user)
        payload = {"mealCount": 200}

        response = self.client.patch(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["mealCount"], 200)

    def test_update_waste_measurement_via_oauth2(self):
        """
        Canteen managers can edit the waste measurement of a canteen they manage via oauth2 token
        """
        user, token = get_oauth2_token("waste_measurements:write")
        self.canteen.managers.add(user)
        payload = {"mealCount": 200}

        self.client.credentials(Authorization=f"Bearer {token}")
        response = self.client.patch(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["mealCount"], 200)

    @authenticate
    @freeze_time("2024-08-10")
    def test_cannot_update_date_to_future(self):
        """
        The period end date cannot be updated to be in the future
        """
        self.canteen.managers.add(authenticate.user)
        measurement = WasteMeasurementFactory(
            canteen=self.canteen, period_start_date="2024-08-01", period_end_date="2024-08-05"
        )
        payload = {"period_end_date": "2024-08-20"}

        response = self.client.patch(
            reverse("canteen_waste_measurement_detail", kwargs={"pk": measurement.id, "canteen_pk": self.canteen.id}),
            payload,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["periodEndDate"][0], "La date ne peut pas être dans le futur")

    @authenticate
    def test_start_date_must_be_before_end_date_in_update(self):
        """
        The period start date must be before end date in update
        """
        self.canteen.managers.add(authenticate.user)
        measurement = WasteMeasurementFactory(
            canteen=self.canteen,
            period_start_date=datetime.date(2024, 8, 1),
            period_end_date=datetime.date(2024, 8, 5),
        )

        # change start_date to after end_date
        payload = {"period_start_date": "2024-08-10"}

        response = self.client.patch(
            reverse("canteen_waste_measurement_detail", kwargs={"pk": measurement.id, "canteen_pk": self.canteen.id}),
            payload,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["periodStartDate"][0], "La date de début ne peut pas être après la date de fin"
        )

        # change end_date to before start_date
        payload = {"period_end_date": "2024-07-31"}

        response = self.client.patch(
            reverse("canteen_waste_measurement_detail", kwargs={"pk": measurement.id, "canteen_pk": self.canteen.id}),
            payload,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["periodStartDate"][0], "La date de début ne peut pas être après la date de fin"
        )

    @authenticate
    def test_periods_cannot_overlap_in_update(self):
        """
        A measurement update cannot have a period that overlaps with an existing measurement
        """
        self.canteen.managers.add(authenticate.user)
        WasteMeasurementFactory(
            canteen=self.canteen,
            period_start_date=datetime.date(2024, 7, 1),
            period_end_date=datetime.date(2024, 7, 5),
        )

        # check a start date that falls in existing period
        measurement = WasteMeasurementFactory(
            canteen=self.canteen,
            period_start_date=datetime.date(2024, 8, 1),
            period_end_date=datetime.date(2024, 8, 5),
        )
        payload = {"period_start_date": "2024-07-03"}

        response = self.client.patch(
            reverse("canteen_waste_measurement_detail", kwargs={"pk": measurement.id, "canteen_pk": self.canteen.id}),
            payload,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["_All__"][0],
            "Il existe déjà une autre évaluation dans la période 2024-07-03 à 2024-08-05. Veuillez modifier l'évaluation existante ou corriger les dates de la période.",
        )

        # check an end date that falls in existing period
        measurement = WasteMeasurementFactory(
            canteen=self.canteen,
            period_start_date=datetime.date(2024, 6, 1),
            period_end_date=datetime.date(2024, 6, 5),
        )
        payload = {"period_end_date": "2024-07-03"}

        response = self.client.patch(
            reverse("canteen_waste_measurement_detail", kwargs={"pk": measurement.id, "canteen_pk": self.canteen.id}),
            payload,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["_All__"][0],
            "Il existe déjà une autre évaluation dans la période 2024-06-01 à 2024-07-03. Veuillez modifier l'évaluation existante ou corriger les dates de la période.",
        )

        # check a start and end date that encapsulate the periods of existing measurements
        payload = {
            "period_start_date": "2024-01-30",
            "period_end_date": "2024-08-10",
        }

        response = self.client.patch(
            reverse("canteen_waste_measurement_detail", kwargs={"pk": measurement.id, "canteen_pk": self.canteen.id}),
            payload,
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
        self.canteen.managers.add(authenticate.user)
        measurement = WasteMeasurementFactory(
            canteen=self.canteen,
            period_start_date=datetime.date(2024, 7, 1),
            period_end_date=datetime.date(2024, 7, 5),
        )

        payload = {
            "period_start_date": None,
            "period_end_date": "",
        }

        response = self.client.patch(
            reverse("canteen_waste_measurement_detail", kwargs={"pk": measurement.id, "canteen_pk": self.canteen.id}),
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
        canteen = CanteenFactory(managers=[authenticate.user])
        measurement = WasteMeasurementFactory(
            canteen=canteen, period_start_date=datetime.date(2024, 5, 1), period_end_date=datetime.date(2024, 5, 10)
        )

        payload = {"period_start_date": "2024-04-01", "period_end_date": "2024-07-01"}
        response = self.client.patch(
            reverse("canteen_waste_measurement_detail", kwargs={"pk": measurement.id, "canteen_pk": canteen.id}),
            payload,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        measurement.refresh_from_db()
        self.assertEqual(measurement.period_start_date, datetime.date(2024, 4, 1))
        self.assertEqual(measurement.period_end_date, datetime.date(2024, 7, 1))


class WasteMeasurementsDeleteApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        cls.measurement = WasteMeasurementFactory(
            canteen=cls.canteen,
            meal_count=100,
            period_start_date=datetime.date(2023, 1, 1),
            period_end_date=datetime.date(2023, 1, 5),
        )
        cls.url = reverse(
            "canteen_waste_measurement_detail", kwargs={"pk": cls.measurement.id, "canteen_pk": cls.canteen.id}
        )

    @authenticate
    def test_cannot_delete_waste_measurement(self):
        """
        Canteen managers cannot delete waste measurements
        """
        self.canteen.managers.add(authenticate.user)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
