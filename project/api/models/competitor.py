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
from ranking import Ranking
from django.utils.functional import cached_property
from django.urls import reverse

# Django
from django.db import models

from api.tasks import create_csa_report
from api.fields import UploadPath
from api.tasks import save_csa_report

log = logging.getLogger(__name__)


class Competitor(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    STATUS = Choices(
        (-30, 'disqualified', 'Disqualified',),
        (-20, 'scratched', 'Scratched',),
        (-10, 'finished', 'Finished',),
        (0, 'new', 'New',),
        (10, 'started', 'Started',),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
        choices=STATUS,
        default=STATUS.new,
    )

    image = models.ImageField(
        upload_to=UploadPath(),
        null=True,
        blank=True,
    )

    is_ranked = models.BooleanField(
        help_text="""If the competitor will be ranked in OSS.""",
        default=False,
    )

    is_multi = models.BooleanField(
        help_text="""If the competitor is contesting a multi-round award.""",
        default=False,
    )

    pos = models.IntegerField(
        help_text='Actual Participants-on-Stage',
        null=True,
        blank=True,
    )

    draw = models.IntegerField(
        null=True,
        blank=True,
    )

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

    mus_rank = models.IntegerField(
        null=True,
        blank=True,
    )

    per_rank = models.IntegerField(
        null=True,
        blank=True,
    )

    sng_rank = models.IntegerField(
        null=True,
        blank=True,
    )

    tot_rank = models.IntegerField(
        null=True,
        blank=True,
    )

    csa_report = models.FileField(
        null=True,
        blank=True,
    )

    # FKs
    session = models.ForeignKey(
        'Session',
        related_name='competitors',
        on_delete=models.CASCADE,
    )

    group = models.ForeignKey(
        'Group',
        related_name='competitors',
        on_delete=models.CASCADE,
    )

    entry = models.OneToOneField(
        'Entry',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    @cached_property
    def csa(self):
        return reverse(
            'competitor-csa',
            args=[str(self.id)]
        )

    # Internals
    class Meta:
        verbose_name_plural = 'competitors'
        unique_together = (
            ('group', 'session',),
        )

    class JSONAPIMeta:
        resource_name = "competitor"

    def __str__(self):
        return "{0} {1}".format(
            self.session,
            self.group.name,
        )

    # Competitor Permissions
    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_read_permission(self, request):
        return any([
            self.session.convention.assignments.filter(
                person__user=request.user,
                status__gt=0,
                category__lte=10,
            ),
            self.status == self.STATUS.finished,
        ])

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.is_round_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            all([
                self.session.convention.assignments.filter(
                    person__user=request.user,
                    status__gt=0,
                    category__lte=10,
                ),
                self.status != self.STATUS.finished,
            ]),
        ])

    # Competitor Methods
    def calculate(self):
        self.mus_points = self.appearances.filter(
            songs__scores__kind=10,
            songs__scores__category=30,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']
        self.per_points = self.appearances.filter(
            songs__scores__kind=10,
            songs__scores__category=40,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']
        self.sng_points = self.appearances.filter(
            songs__scores__kind=10,
            songs__scores__category=50,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']

        self.tot_points = self.appearances.filter(
            songs__scores__kind=10,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']
        self.mus_score = self.appearances.filter(
            songs__scores__kind=10,
            songs__scores__category=30,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']
        self.per_score = self.appearances.filter(
            songs__scores__kind=10,
            songs__scores__category=40,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']
        self.sng_score = self.appearances.filter(
            songs__scores__kind=10,
            songs__scores__category=50,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']
        self.tot_score = self.appearances.filter(
            songs__scores__kind=10,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']

    # Competitor Transition Conditions

    # Competitor Transitions
    @fsm_log_by
    @transition(
        field=status,
        source=[STATUS.new, STATUS.started, STATUS.finished],
        target=STATUS.started,
    )
    def start(self, *args, **kwargs):
        self.csa_report.delete()
        return

    @fsm_log_by
    @transition(
        field=status,
        source=[STATUS.new, STATUS.started, STATUS.finished],
        target=STATUS.finished,
    )
    def finish(self, *args, **kwargs):
        return

    @fsm_log_by
    @transition(
        field=status,
        source='*',
        target=STATUS.scratched,
    )
    def scratch(self, *args, **kwargs):
        self.tot_rank = None
        self.mus_rank = None
        self.per_rank = None
        self.sng_rank = None
        self.tot_points = None
        self.mus_points = None
        self.per_points = None
        self.sng_points = None
        self.tot_score = None
        self.mus_score = None
        self.per_score = None
        self.sng_score = None
        appearances = self.appearances.all()
        appearances.delete()
        return

    @fsm_log_by
    @transition(
        field=status,
        source='*',
        target=STATUS.disqualified,
    )
    def disqualify(self, *args, **kwargs):
        return
