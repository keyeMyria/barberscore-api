# Standard Libary
import logging
import uuid

# Third-Party
from django_fsm import FSMIntegerField
from django_fsm import transition
from django_fsm_log.decorators import fsm_log_by
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices
from model_utils.models import TimeStampedModel

# Django
from django.apps import apps as api_apps
from django.db import models
from django.utils.encoding import smart_text

config = api_apps.get_app_config('api')

log = logging.getLogger(__name__)


class Contestant(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        editable=False,
    )

    STATUS = Choices(
        (-10, 'excluded', 'Excluded',),
        (0, 'new', 'New',),
        (10, 'included', 'Included',),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
        choices=STATUS,
        default=STATUS.new,
    )

    # Privates
    rank = models.IntegerField(
        null=True,
        blank=True,
    )

    mus_points = models.IntegerField(
        null=True,
        blank=True,
    )

    per_points = models.IntegerField(
        null=True,
        blank=True,
    )

    sng_points = models.IntegerField(
        null=True,
        blank=True,
    )

    tot_points = models.IntegerField(
        null=True,
        blank=True,
    )

    mus_score = models.FloatField(
        null=True,
        blank=True,
    )

    per_score = models.FloatField(
        null=True,
        blank=True,
    )

    sng_score = models.FloatField(
        null=True,
        blank=True,
    )

    tot_score = models.FloatField(
        null=True,
        blank=True,
    )

    # FKs
    entry = models.ForeignKey(
        'Entry',
        related_name='contestants',
        on_delete=models.CASCADE,
    )

    contest = models.ForeignKey(
        'Contest',
        related_name='contestants',
        on_delete=models.CASCADE,
    )

    # Internals
    class Meta:
        unique_together = (
            ('entry', 'contest',),
        )

    class JSONAPIMeta:
        resource_name = "contestant"

    def __str__(self):
        return self.nomen if self.nomen else str(self.pk)

    def save(self, *args, **kwargs):
        self.nomen = " ".join(
            map(
                lambda x: smart_text(x), [
                    self.entry,
                    self.contest,
                ]
            )
        )
        super().save(*args, **kwargs)

    # Methods
    def calculate(self, *args, **kwargs):
        self.mus_points = self.calculate_mus_points()
        self.per_points = self.calculate_per_points()
        self.sng_points = self.calculate_sng_points()
        self.tot_points = self.calculate_tot_points()
        self.mus_score = self.calculate_mus_score()
        self.per_score = self.calculate_per_score()
        self.sng_score = self.calculate_sng_score()
        self.tot_score = self.calculate_tot_score()
        self.rank = self.calculate_rank()

    # def calculate_rank(self):
    #     return self.contest.ranking(self.calculate_tot_points())

    def calculate_mus_points(self):
        return self.entry.appearances.filter(
            songs__scores__kind=10,
            songs__scores__category=30,
            round__num__lte=self.contest.award.rounds,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']

    def calculate_per_points(self):
        return self.entry.appearances.filter(
            songs__scores__kind=10,
            songs__scores__category=40,
            round__num__lte=self.contest.award.rounds,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']

    def calculate_sng_points(self):
        return self.entry.appearances.filter(
            songs__scores__kind=10,
            songs__scores__category=50,
            round__num__lte=self.contest.award.rounds,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']

    def calculate_tot_points(self):
        return self.entry.appearances.filter(
            songs__scores__kind=10,
            round__num__lte=self.contest.award.rounds,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']

    def calculate_mus_score(self):
        return self.entry.appearances.filter(
            songs__scores__kind=10,
            songs__scores__category=30,
            round__num__lte=self.contest.award.rounds,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']

    def calculate_per_score(self):
        return self.entry.appearances.filter(
            songs__scores__kind=10,
            songs__scores__category=40,
            round__num__lte=self.contest.award.rounds,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']

    def calculate_sng_score(self):
        return self.entry.appearances.filter(
            songs__scores__kind=10,
            songs__scores__category=50,
            round__num__lte=self.contest.award.rounds,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']

    def calculate_tot_score(self):
        return self.entry.appearances.filter(
            songs__scores__kind=10,
            round__num__lte=self.contest.award.rounds,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.is_convention_manager,
            request.user.is_group_manager,
            request.user.is_session_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            self.contest.session.convention.assignments.filter(
                person__user=request.user,
                category__lte=10,
                kind=10,
            ),
            self.entry.group.organization.officers.filter(
                person__user=request.user,
                status__gt=0,
            ),
        ])

    # Methods

    # Contestant Transitions
    @fsm_log_by
    @transition(field=status, source=[STATUS.new, STATUS.excluded], target=STATUS.included)
    def include(self, *args, **kwargs):
        return

    @fsm_log_by
    @transition(field=status, source=[STATUS.new, STATUS.included], target=STATUS.excluded)
    def exclude(self, *args, **kwargs):
        return