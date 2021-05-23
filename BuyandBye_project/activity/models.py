from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

from .options import ACTION_CHOICES


class Activity(models.Model):
    user = models.ForeignKey(
        User, related_name="activity", db_index=True, on_delete=models.CASCADE
    )
    verb = models.CharField(max_length=250, choices=ACTION_CHOICES)
    target_ct = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        related_name="target_obj",
        on_delete=models.CASCADE,
    )
    target_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    # target_name = models.CharField(max_length=200, null=True, blank=True)
    target = GenericForeignKey("target_ct", "target_id")

    date_created = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        verbose_name_plural = "Activities"
        ordering = ("-date_created",)

    def __str__(self):
        # return self.subname returns the non human readable tuple
        return f"Activity: {self.user} {self.verb} {self.target} target_ct: {self.target_ct_id} ({self.id})"
