""" Activity utility functions """
import datetime

from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from .models import Activity


def create_action(user, verb, target=None):
    """ create an activity action like viewing post while checking duplication """

    # check duplicates
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Activity.objects.filter(
        user_id=user.id, verb=verb, date_created__gte=last_minute
    )

    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(
            target_ct=target_ct, target_id=target.id
        )

    if not similar_actions:
        action = Activity(user=user, verb=verb, target=target)
        action.save()
        return True

    return False
