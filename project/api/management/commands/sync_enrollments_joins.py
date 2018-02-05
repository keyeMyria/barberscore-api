import logging
import django_rq
# Django
from django.core.management.base import BaseCommand

# First-Party
from api.models import Enrollment
from bhs.models import SMJoin

log = logging.getLogger('updater')


class Command(BaseCommand):
    help = "Command to sync quartets and structures."

    def handle(self, *args, **options):
        self.stdout.write("Updating chapter enrollments...")

        # Get unique active joins for Chapters
        dicts = SMJoin.objects.filter(
            inactive_date=None,
            structure__kind='Chapter',
        ).values(
            'id',
            'subscription__human',
            'structure',
        ).distinct()
        ids_list = [a['id'] for a in dicts]
        joins = SMJoin.objects.filter(
            id__in=ids_list,
        )
        # Creating/Update Groups
        self.stdout.write("Queuing enrollment updates...")
        for join in joins:
            django_rq.enqueue(
                Enrollment.objects.update_or_create_from_join,
                join,
            )
        self.stdout.write("Complete")
