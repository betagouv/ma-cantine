from unittest import mock

from django.test import RequestFactory, SimpleTestCase
from django.urls import resolve, reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import authenticate, get_oauth2_token
from data.factories import CanteenFactory
from data.models import EventLog
from macantine.middleware import EventLogMiddleware


class EventLogMiddlewareTest(APITestCase):
    def setUp(self):
        self.canteen = CanteenFactory()
        self.url = reverse("single_canteen", kwargs={"pk": self.canteen.id})

    def test_oauth2_write_request_success_is_logged(self):
        user, token = get_oauth2_token("canteen:write")
        self.canteen.managers.add(user)
        self.client.credentials(Authorization=f"Bearer {token.token}")

        response = self.client.patch(self.url, {"name": "Nouveau nom"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        event_log = EventLog.objects.get()
        self.assertEqual(event_log.category, EventLog.Category.API)
        self.assertEqual(event_log.status, EventLog.Status.SUCCESS)
        self.assertEqual(event_log.name, "PATCH /api/v1/canteens/{id}")
        self.assertEqual(event_log.user, user)
        self.assertEqual(event_log.api_oauth2_application, token.application)
        self.assertEqual(set(event_log.data.keys()), {"method", "path", "status_code", "seconds", "message"})
        self.assertEqual(event_log.data["method"], "PATCH")
        self.assertEqual(event_log.data["path"], f"/api/v1/canteens/{self.canteen.id}")
        self.assertEqual(event_log.data["status_code"], 200)
        self.assertIsNone(event_log.data["message"])

    def test_oauth2_write_request_failure_is_logged(self):
        user, token = get_oauth2_token("canteen:write")
        self.canteen.managers.add(user)
        self.client.credentials(Authorization=f"Bearer {token.token}")

        response = self.client.patch(self.url, {"dailyMealCount": "pas un nombre"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        event_log = EventLog.objects.get()
        self.assertEqual(event_log.status, EventLog.Status.FAILURE)
        self.assertEqual(event_log.data["status_code"], 400)
        self.assertIn("dailyMealCount", event_log.data["message"])

    def test_oauth2_write_request_without_scope_is_logged(self):
        user, token = get_oauth2_token("canteen:read")
        self.canteen.managers.add(user)
        self.client.credentials(Authorization=f"Bearer {token.token}")

        response = self.client.patch(self.url, {"name": "Nouveau nom"})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        event_log = EventLog.objects.get()
        self.assertEqual(event_log.status, EventLog.Status.FAILURE)
        self.assertEqual(event_log.api_oauth2_application, token.application)
        self.assertEqual(event_log.data["status_code"], 403)

    def test_oauth2_read_request_is_not_logged(self):
        user, token = get_oauth2_token("canteen:read")
        self.canteen.managers.add(user)
        self.client.credentials(Authorization=f"Bearer {token.token}")

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(EventLog.objects.exists())

    @authenticate
    def test_web_app_write_request_is_not_logged(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.patch(self.url, {"name": "Nouveau nom"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(EventLog.objects.exists())

    def test_logging_error_does_not_break_the_request(self):
        user, token = get_oauth2_token("canteen:write")
        self.canteen.managers.add(user)
        self.client.credentials(Authorization=f"Bearer {token.token}")

        with mock.patch("macantine.middleware.event_log_middleware.EventLog.log", side_effect=Exception("DB down")):
            response = self.client.patch(self.url, {"name": "Nouveau nom"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.canteen.refresh_from_db()
        self.assertEqual(self.canteen.name, "Nouveau nom")


class EventLogMiddlewareRouteTest(SimpleTestCase):
    def get_route(self, path):
        request = RequestFactory().patch(path)
        request.resolver_match = resolve(path)
        return EventLogMiddleware._get_route(request)

    def test_route_in_openapi_format(self):
        # same format as the OpenAPI schema (/api/docs/): parameters in braces, pk renamed to id
        self.assertEqual(self.get_route("/api/v1/canteens/12"), "/api/v1/canteens/{id}")
        self.assertEqual(
            self.get_route("/api/v1/canteens/12/diagnostics/34"), "/api/v1/canteens/{canteen_pk}/diagnostics/{id}"
        )
        self.assertEqual(
            self.get_route("/api/v1/canteens/12/purchases/34/facture"),
            "/api/v1/canteens/{canteen_pk}/purchases/{id}/facture",
        )
        self.assertEqual(
            self.get_route("/api/v1/canteens/12/purchases/summary/2025"),
            "/api/v1/canteens/{canteen_pk}/purchases/summary/{year}",
        )
        self.assertEqual(self.get_route("/api/v1/canteens/"), "/api/v1/canteens/")

    def test_route_fallback_to_path(self):
        request = RequestFactory().patch("/api/v1/unknown/12")
        request.resolver_match = None

        self.assertEqual(EventLogMiddleware._get_route(request), "/api/v1/unknown/12")
