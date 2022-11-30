from django.contrib.sitemaps import Sitemap
from data.models import Canteen, BlogPost, Partner


class CanteenSitemap(Sitemap):
    def items(self):
        return Canteen.objects.filter(publication_status="published").order_by("id")

    def location(self, obj):
        return obj.url_path

    def lastmod(self, obj):
        return obj.modification_date

    def changefreq(self, obj):
        return "weekly"

    def priority(self, obj):
        return 0.5


class BlogPostSitemap(Sitemap):
    def items(self):
        return BlogPost.objects.filter(published=True).order_by("id")

    def location(self, obj):
        return obj.url_path

    def lastmod(self, obj):
        return obj.modification_date

    def changefreq(self, obj):
        return "monthly"

    def priority(self, obj):
        return 0.5


class PartnerSitemap(Sitemap):
    def items(self):
        return Partner.objects.filter(published=True).order_by("id")

    def location(self, obj):
        return obj.url_path

    def lastmod(self, obj):
        return obj.modification_date

    def changefreq(self, obj):
        return "monthly"

    def priority(self, obj):
        return 0.4


class WebSitemap(Sitemap):
    def items(self):
        return [
            {"location": "/accueil", "changefreq": "yearly", "priority": 1.0},
            {"location": "/diagnostic", "changefreq": "yearly", "priority": 0.3},
            {"location": "/creation-affiche", "changefreq": "yearly", "priority": 0.4},
            {"location": "/mesures-phares", "changefreq": "yearly", "priority": 0.3},
            {
                "location": "/mesures-phares/qualite-des-produits",
                "changefreq": "yearly",
                "priority": 0.4,
            },
            {
                "location": "/mesures-phares/gaspillage-alimentaire",
                "changefreq": "yearly",
                "priority": 0.4,
            },
            {
                "location": "/mesures-phares/diversification-des-menus",
                "changefreq": "yearly",
                "priority": 0.4,
            },
            {
                "location": "/mesures-phares/interdiction-du-plastique",
                "changefreq": "yearly",
                "priority": 0.4,
            },
            {
                "location": "/mesures-phares/information-des-usagers",
                "changefreq": "yearly",
                "priority": 0.4,
            },
            {"location": "/nos-cantines", "changefreq": "weekly", "priority": 0.5},
            {"location": "/mentions-legales", "changefreq": "yearly", "priority": 0.2},
            {"location": "/cgu", "changefreq": "yearly", "priority": 0.2},
            {"location": "/blog", "changefreq": "monthly", "priority": 0.5},
            {"location": "/communaute", "changefreq": "monthly", "priority": 0.5},
            {"location": "/acteurs-de-l-eco-systeme", "changefreq": "monthly", "priority": 0.4},
            {"location": "/statistiques-regionales", "changefreq": "monthly", "priority": 0.3},
            {"location": "/statistiques-plateforme", "changefreq": "monthly", "priority": 0.3},
            {"location": "/creer-mon-compte", "changefreq": "yearly", "priority": 0.3},
            {"location": "/s-identifier", "changefreq": "yearly", "priority": 0.3},
        ]

    def location(self, obj):
        return obj.get("location")

    def changefreq(self, obj):
        return obj.get("changefreq")

    def priority(self, obj):
        return obj.get("priority")
