from django.contrib import admin
from data.models import Message
from .utils import ReadOnlyAdminMixin


@admin.action(description="Valider et envoyer")
def send(modeladmin, request, queryset):
    [message.send() for message in queryset]


@admin.action(description="Bloquer")
def block(modeladmin, request, queryset):
    [message.block() for message in queryset]


class MessageStatusFilter(admin.SimpleListFilter):
    title = "Statut du message"
    parameter_name = "status"

    def lookups(self, request, model_admin):
        return (
            (None, "⌛ En attente"),
            ("SENT", "✅ Envoyé"),
            ("BLOCKED", "🛑 Bloqué"),
            ("ALL", "Tous"),
        )

    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                "selected": self.value() == lookup,
                "query_string": cl.get_query_string(
                    {
                        self.parameter_name: lookup,
                    },
                    [],
                ),
                "display": title,
            }

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset.filter(status=Message.Status.PENDING)
        elif self.value() in ("all"):
            return queryset
        elif self.value() in ("SENT"):
            return queryset.filter(status=Message.Status.SENT)
        elif self.value() in ("BLOCKED"):
            return queryset.filter(status=Message.Status.BLOCKED)


@admin.register(Message)
class MessageAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    fields = (
        "creation_date",
        "destination_canteen",
        "sender_name",
        "sender_email",
        "body",
        "statut",
        "sent_date",
    )
    read_only_fields = fields
    list_display = (
        "body",
        "sender_email",
        "destinataire",
        "statut",
    )
    list_filter = (MessageStatusFilter,)
    actions = [send, block]

    def destinataire(self, obj):
        return obj.destination_canteen.name if obj.destination_canteen else "⚠️ Cantine inconnue"

    def statut(self, obj):
        if obj.status == Message.Status.PENDING:
            return "⌛ En attente"
        if obj.status == Message.Status.SENT:
            return "✅ Envoyé"
        if obj.status == Message.Status.BLOCKED:
            return "🛑 Bloqué"
