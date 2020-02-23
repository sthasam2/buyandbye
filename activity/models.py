from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.utils import timezone

from .options import ACTION_CHOICES


class Activity(models.Model):
    user = models.ForeignKey(
        User, related_name='activity', db_index=True, on_delete=models.CASCADE)
    verb = models.CharField(max_length=250, choices=ACTION_CHOICES)
    target_ct = models.ForeignKey(
        ContentType, blank=True, null=True, related_name='target_obj', on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(
        null=True, blank=True, db_index=True)
    target = GenericForeignKey('target_ct', 'target_id')

    date_created = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ('-date_created',)
