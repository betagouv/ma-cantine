from django.db import models


# These unmanaged Django models mirror Kombu's SQLAlchemy transport tables.
# Docs: https://docs.celeryq.dev/projects/kombu/en/stable/reference/kombu.transport.sqlalchemy.html
# Source schema: kombu/transport/sqlalchemy/models.py in the installed Kombu package.
class KombuQueue(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        managed = False
        db_table = "kombu_queue"
        verbose_name = "Kombu queue"
        verbose_name_plural = "Kombu queues"

    def __str__(self):
        return self.name


class KombuMessage(models.Model):
    id = models.AutoField(primary_key=True)
    visible = models.BooleanField(default=True)
    sent_at = models.DateTimeField(db_column="timestamp", null=True, blank=True)
    payload = models.TextField()
    version = models.SmallIntegerField(default=1)
    queue = models.ForeignKey(KombuQueue, models.DO_NOTHING, db_column="queue_id", related_name="messages")

    class Meta:
        managed = False
        db_table = "kombu_message"
        verbose_name = "Kombu message"
        verbose_name_plural = "Kombu messages"

    def __str__(self):
        return f"Message {self.id} ({self.queue_id})"
