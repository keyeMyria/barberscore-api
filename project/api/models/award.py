
# Standard Library
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
from django.contrib.postgres.fields import FloatRangeField
from django.contrib.postgres.fields import IntegerRangeField
from django.core.exceptions import ValidationError
from django.db import models

# First-Party
from api.managers import AwardManager

log = logging.getLogger(__name__)


class Award(TimeStampedModel):
    """
    Award Model.

    The specific award conferred by a Group.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        help_text="""Award Name.""",
        max_length=255,
    )

    STATUS = Choices(
        (-10, 'inactive', 'Inactive',),
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
        choices=STATUS,
        default=STATUS.new,
    )

    KIND = Choices(
        (32, 'chorus', "Chorus"),
        (41, 'quartet', "Quartet"),
    )

    kind = models.IntegerField(
        choices=KIND,
    )

    GENDER = Choices(
        (10, 'male', "Male"),
        (20, 'female', "Female"),
        (30, 'mixed', "Mixed"),
    )

    gender = models.IntegerField(
        help_text="""
            The gender of session.
        """,
        choices=GENDER,
        default=GENDER.male,
    )

    LEVEL = Choices(
        (10, 'championship', "Championship"),
        (30, 'qualifier', "Qualifier"),
        (35, 'top', "Top"),
        (40, 'award', "Award"),
        (45, 'representative', "Representative"),
        (50, 'deferred', "Deferred"),
        (60, 'manual', "Manual"),
    )

    level = models.IntegerField(
        choices=LEVEL,
    )

    SEASON = Choices(
        (1, 'summer', 'Summer',),
        (2, 'midwinter', 'Midwinter',),
        (3, 'fall', 'Fall',),
        (4, 'spring', 'Spring',),
        (9, 'video', 'Video',),
    )

    season = models.IntegerField(
        choices=SEASON,
    )

    rounds = models.IntegerField(
        help_text="""Number of rounds to determine the championship""",
    )

    threshold = models.FloatField(
        help_text="""
            The score threshold for automatic qualification (if any.)
        """,
        null=True,
        blank=True,
    )

    minimum = models.FloatField(
        help_text="""
            The minimum score required for qualification (if any.)
        """,
        null=True,
        blank=True,
    )

    advance = models.FloatField(
        help_text="""
            The score threshold to advance to next round (if any) in
            multi-round qualification.
        """,
        null=True,
        blank=True,
    )

    spots = models.IntegerField(
        help_text="""Number of top spots which qualify""",
        null=True,
        blank=True,
    )

    description = models.TextField(
        help_text="""
            The Public description of the award.""",
        blank=True,
        max_length=1000,
    )

    notes = models.TextField(
        help_text="""
            Private Notes (for internal use only).""",
        blank=True,
    )

    AGE = Choices(
        (10, 'seniors', 'Seniors',),
        (30, 'youth', 'Youth',),
    )

    age = models.IntegerField(
        choices=AGE,
        null=True,
        blank=True,
    )

    SIZE = Choices(
        (100, 'p1', 'Plateau 1',),
        (110, 'p2', 'Plateau 2',),
        (120, 'p3', 'Plateau 3',),
        (130, 'p4', 'Plateau 4',),
        (140, 'pa', 'Plateau A',),
        (150, 'paa', 'Plateau AA',),
        (160, 'paaa', 'Plateau AAA',),
        (170, 'paaaa', 'Plateau AAAA',),
        (180, 'pb', 'Plateau B',),
        (190, 'pi', 'Plateau I',),
        (200, 'pii', 'Plateau II',),
        (210, 'piii', 'Plateau III',),
        (220, 'piv', 'Plateau IV',),
        (230, 'small', 'Small',),
    )

    size = models.IntegerField(
        choices=SIZE,
        null=True,
        blank=True,
    )

    size_range = IntegerRangeField(
        null=True,
        blank=True,
    )

    SCOPE = Choices(
        (100, 'p1', 'Plateau 1',),
        (110, 'p2', 'Plateau 2',),
        (120, 'p3', 'Plateau 3',),
        (130, 'p4', 'Plateau 4',),
        (140, 'pa', 'Plateau A',),
        (150, 'paa', 'Plateau AA',),
        (160, 'paaa', 'Plateau AAA',),
        (170, 'paaaa', 'Plateau AAAA',),
        (175, 'paaaaa', 'Plateau AAAAA',),
    )

    scope = models.IntegerField(
        choices=SCOPE,
        null=True,
        blank=True,
    )

    scope_range = FloatRangeField(
        null=True,
        blank=True,
    )

    # Denormalizations
    tree_sort = models.IntegerField(
        unique=True,
        blank=True,
        null=True,
        editable=False,
    )

    # FKs
    group = models.ForeignKey(
        'Group',
        related_name='awards',
        on_delete=models.CASCADE,
    )

    parent = models.ForeignKey(
        'self',
        help_text="""If a qualifier, this is the award qualifying for.""",
        related_name='children',
        null=True,
        blank=True,
        db_index=True,
        on_delete=models.SET_NULL,
    )

    # Internals
    objects = AwardManager()

    class Meta:
        ordering = [
            'tree_sort',
        ]

    class JSONAPIMeta:
        resource_name = "award"

    def __str__(self):
        return self.name

    def clean(self):
        pass
        # if self.level == self.LEVEL.qualifier and not self.threshold:
        #     raise ValidationError(
        #         {'level': 'Qualifiers must have thresholds'}
        #     )
        # if self.level != self.LEVEL.qualifier and self.threshold:
        #     raise ValidationError(
        #         {'level': 'Non-Qualifiers must not have thresholds'}
        #     )

    # Award Permissions
    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.is_award_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            request.user.is_award_manager,
        ])

    # Transitions
    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.active)
    def activate(self, *args, **kwargs):
        """Activate the Award."""
        return

    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.inactive)
    def deactivate(self, *args, **kwargs):
        """Deactivate the Award."""
        return
