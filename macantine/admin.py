from django.contrib import admin
from django.contrib.admin import AdminSite
from django.urls import path, reverse

from data.admin.sector import sector_textchoices_admin_view
from data.admin.textchoices import CANTEEN_TEXTCHOICES_PAGES, canteen_textchoices_admin_view


class MaCantineAdminSite(AdminSite):
    """
    Custom AdminSite to inject synthetic, read-only entries in the app list
    """

    def get_urls(self):
        custom_urls = [
            path(
                "data/sector-textchoices/",
                self.admin_view(sector_textchoices_admin_view),
                name="sector-textchoices",
            ),
            path(
                "data/canteen-<slug:page_key>-textchoices/",
                self.admin_view(canteen_textchoices_admin_view),
                name="canteen-textchoices",
            ),
        ]
        return custom_urls + super().get_urls()

    def _get_synthetic_data_models(self):
        models = [
            {
                "name": "Secteurs d'activité (TextChoices)",
                "object_name": "SectorTextChoices",
                "perms": {"add": False, "change": False, "delete": False, "view": True},
                "admin_url": reverse("admin:sector-textchoices"),
                "add_url": None,
                "view_only": True,
            }
        ]

        for page in CANTEEN_TEXTCHOICES_PAGES:
            models.append(
                {
                    "name": page["title"],
                    "object_name": page["object_name"],
                    "perms": {"add": False, "change": False, "delete": False, "view": True},
                    "admin_url": reverse("admin:canteen-textchoices", kwargs={"page_key": page["key"]}),
                    "add_url": None,
                    "view_only": True,
                }
            )
        return models

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, app_label)

        if app_label and app_label != "data":
            return app_list

        synthetic_models = self._get_synthetic_data_models()

        data_app = next((app for app in app_list if app.get("app_label") == "data"), None)
        if data_app:
            existing_by_object_name = {model.get("object_name") for model in data_app["models"]}
            for synthetic_model in synthetic_models:
                if synthetic_model["object_name"] not in existing_by_object_name:
                    data_app["models"].append(synthetic_model)
            data_app["models"].sort(key=lambda model: model.get("name", "").lower())
            return app_list

        if request.user.has_module_perms("data"):
            app_list.append(
                {
                    "name": "Data",
                    "app_label": "data",
                    "app_url": reverse("admin:app_list", kwargs={"app_label": "data"}),
                    "has_module_perms": True,
                    "models": sorted(synthetic_models, key=lambda model: model.get("name", "").lower()),
                }
            )

        return app_list


admin.site.__class__ = MaCantineAdminSite
