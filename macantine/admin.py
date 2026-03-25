from django.contrib.admin import AdminSite
from django.contrib import admin
from django.urls import path, reverse

from data.admin.sector import sector_textchoices_admin_view


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
            )
        ]
        return custom_urls + super().get_urls()

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, app_label)

        if app_label and app_label != "data":
            return app_list

        sector_textchoices_model = {
            "name": "Secteurs d'activité (TextChoices)",
            "object_name": "SectorTextChoices",
            "perms": {"add": False, "change": False, "delete": False, "view": True},
            "admin_url": reverse("admin:sector-textchoices"),
            "add_url": None,
            "view_only": True,
        }

        data_app = next((app for app in app_list if app.get("app_label") == "data"), None)
        if data_app:
            already_present = any(model.get("object_name") == "SectorTextChoices" for model in data_app["models"])
            if not already_present:
                data_app["models"].append(sector_textchoices_model)
                data_app["models"].sort(key=lambda model: model.get("name", "").lower())
            return app_list

        if request.user.has_module_perms("data"):
            app_list.append(
                {
                    "name": "Data",
                    "app_label": "data",
                    "app_url": reverse("admin:app_list", kwargs={"app_label": "data"}),
                    "has_module_perms": True,
                    "models": [sector_textchoices_model],
                }
            )

        return app_list


admin.site.__class__ = MaCantineAdminSite
