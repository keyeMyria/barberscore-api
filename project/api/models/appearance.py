
# Standard Library
import uuid
import pydf
from random import randint

# Third-Party
import django_rq
from django_fsm import FSMIntegerField
from django.core.files.base import ContentFile
from django_fsm import transition
from django_fsm import RETURN_VALUE
from django_fsm_log.decorators import fsm_log_by
from django_fsm_log.models import StateLog
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices
from model_utils.models import TimeStampedModel

# Django
from django.apps import apps
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Avg
from django.db.models import Q
from django.db.models import Sum
from django.utils.functional import cached_property
from django.utils.timezone import now
from django.template.loader import render_to_string
from django.utils.text import slugify


class Appearance(TimeStampedModel):
    """
    An appearance of a competitor on stage.

    The Appearance is meant to be a private resource.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (7, 'built', 'Built',),
        (10, 'started', 'Started',),
        (20, 'finished', 'Finished',),
        (25, 'variance', 'Variance',),
        (30, 'verified', 'Verified',),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
        choices=STATUS,
        default=STATUS.new,
    )

    num = models.IntegerField(
        null=True,
        blank=True,
    )

    draw = models.IntegerField(
        null=True,
        blank=True,
    )

    actual_start = models.DateTimeField(
        help_text="""
            The actual appearance window.""",
        null=True,
        blank=True,
    )

    actual_finish = models.DateTimeField(
        help_text="""
            The actual appearance window.""",
        null=True,
        blank=True,
    )

    pos = models.IntegerField(
        help_text='Actual Participants-on-Stage',
        null=True,
        blank=True,
    )

    legacy_group = models.CharField(
        max_length=255,
        blank=True,
        null=True,
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

    variance_report = models.FileField(
        null=True,
        blank=True,
    )

    # Appearance FKs
    round = models.ForeignKey(
        'Round',
        related_name='appearances',
        on_delete=models.CASCADE,
    )

    competitor = models.ForeignKey(
        'Competitor',
        related_name='appearances',
        on_delete=models.CASCADE,
    )

    # Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='appearances',
    )

    @cached_property
    def round__kind(self):
        return self.round.kind

    # Appearance Internals
    def clean(self):
        if self.competitor:
            if self.competitor.group.kind != self.round.session.kind:
                raise ValidationError(
                    {'competitor': 'Competitor kind must match session'}
                )


    class Meta:
        ordering = [
            '-round__num',
            'num',
        ]
        unique_together = (
            ('round', 'num',),
        )

    class JSONAPIMeta:
        resource_name = "appearance"

    def __str__(self):
        return "{0} {1}".format(
            str(self.competitor),
            str(self.round),
        )

    # Methods
    def get_variance(self):
        Score = apps.get_model('api.score')
        Panelist = apps.get_model('api.panelist')
        songs = self.songs.order_by('num')
        scores = Score.objects.filter(
            kind=Score.KIND.official,
            song__in=songs,
        ).order_by(
            'category',
            'panelist__person__last_name',
            'song__num',
        )
        panelists = self.round.panelists.filter(
            kind=Panelist.KIND.official,
            category__gt=Panelist.CATEGORY.ca,
        ).order_by(
            'category',
            'person__last_name',
        )
        context = {
            'appearance': self,
            'songs': songs,
            'scores': scores,
            'panelists': panelists,
        }
        rendered = render_to_string('variance.html', context)
        pdf = pydf.generate_pdf(rendered, enable_smart_shrinking=False)
        content = ContentFile(pdf)
        return content


    def mock(self):
        # Mock Appearance
        Chart = apps.get_model('api.chart')
        prelim = self.competitor.entry.prelim
        if self.competitor.group.kind == self.competitor.group.KIND.chorus:
            pos = self.competitor.group.members.filter(
                status=self.competitor.group.members.model.STATUS.active,
            ).count()
            self.pos = pos
        if not prelim:
            average = self.competitor.group.competitors.filter(
                status=self.competitor.group.competitors.model.STATUS.finished,
            ).aggregate(avg=Avg('tot_score'))['avg']
            if average:
                prelim = average
            else:
                prelim = randint(65, 80)
        songs = self.songs.all()
        for song in songs:
            song.chart = Chart.objects.filter(
                status=Chart.STATUS.active
            ).order_by("?").first()
            song.save()
            scores = song.scores.all()
            for score in scores:
                d = randint(-4, 4)
                score.points = prelim + d
                score.save()
        if self.status == self.STATUS.new:
            raise RuntimeError("Out of state")
        if self.status == self.STATUS.built:
            self.start()
            self.finish()
            self.verify()
            return
        if self.status == self.STATUS.started:
            self.finish()
            self.verify()
            return
        if self.status == self.STATUS.finished:
            self.verify()
            return


    def calculate(self):
        Score = apps.get_model('api.score')
        tot = Sum('points')
        mus = Sum('points', filter=Q(category=Score.CATEGORY.music))
        per = Sum('points', filter=Q(category=Score.CATEGORY.performance))
        sng = Sum('points', filter=Q(category=Score.CATEGORY.singing))
        officials = Score.objects.filter(
            song__appearance=self,
            kind=Score.KIND.official,
        ).annotate(
            tot=tot,
            mus=mus,
            per=per,
            sng=sng,
        )
        tot = officials.aggregate(
            sum=Sum('points'),
            avg=Avg('points'),
        )
        mus = officials.filter(
            category=Score.CATEGORY.music,
        ).aggregate(
            sum=Sum('points'),
            avg=Avg('points'),
        )
        per = officials.filter(
            category=Score.CATEGORY.performance,
        ).aggregate(
            sum=Sum('points'),
            avg=Avg('points'),
        )
        sng = officials.filter(
            category=Score.CATEGORY.singing,
        ).aggregate(
            sum=Sum('points'),
            avg=Avg('points'),
        )
        self.tot_points = tot['sum']
        self.tot_score = tot['avg']
        self.mus_points = mus['sum']
        self.mus_score = mus['avg']
        self.per_points = per['sum']
        self.per_score = per['avg']
        self.sng_points = sng['sum']
        self.sng_score = sng['avg']

    def check_variance(self):
        is_variance = False
        for song in self.songs.all():
            song.calculate()
            # Category Average
            mus_scores = song.scores.filter(
                category=song.scores.model.CATEGORY.music,
            )
            for score in mus_scores:
                if abs(score.points - song.mus_score) > 5:
                    score.is_flagged = True
                    if score.kind == score.KIND.official:
                        is_variance = True
                else:
                    score.is_flagged = False
                score.save()
            per_scores = song.scores.filter(
                category=song.scores.model.CATEGORY.performance,
            )
            for score in per_scores:
                if abs(score.points - song.per_score) > 5:
                    score.is_flagged = True
                    if score.kind == score.KIND.official:
                        is_variance = True
                else:
                    score.is_flagged = False
                score.save()
            sng_scores = song.scores.filter(
                category=song.scores.model.CATEGORY.singing,
            )
            for score in sng_scores:
                if abs(score.points - song.sng_score) > 5:
                    score.is_flagged = True
                    if score.kind == score.KIND.official:
                        is_variance = True
                else:
                    score.is_flagged = False
                score.save()
            if is_variance:
                return True

            # Dixon's Q Test
            confidence = {
                '3': 0.941,
                '6': .56,
                '9': .376,
                '12': .437,
                '15': .338,
            }

            ordered_dsc = song.scores.filter(
                kind=song.scores.model.KIND.official,
            ).order_by('-points')
            spread = ordered_dsc.first().points - ordered_dsc.last().points
            size = str(ordered_dsc.count())

            if size == '3':
                ultimate = ordered_dsc[0]
                penultimate = ordered_dsc[1]
                triultimate = ordered_dsc[2]
                if ultimate.points - penultimate.points >= 10:
                    ultimate.is_flagged = True
                    is_variance = True
                elif penultimate.points - triultimate.points >= 10:
                    triultimate.is_flagged = True
                    is_variance = True
                else:
                    ultimate.is_flagged = False
                    triultimate.is_flagged = False
                ultimate.save()
                triultimate.save()
            else:
                ordered_asc = song.scores.filter(
                    kind=song.scores.model.KIND.official,
                ).order_by('points')
                ultimate = ordered_asc[0]
                penultimate = ordered_asc[1]
                distance = abs(ultimate.points - penultimate.points)
                try:
                    q = distance / spread
                except ZeroDivisionError:
                    q = 0
                critical = confidence[size]
                if q > critical and penultimate.points - ultimate.points > 5:
                    ultimate.is_flagged = True
                    is_variance = True
                else:
                    ultimate.is_flagged = False
                ultimate.save()
                practice_scores = song.scores.filter(
                    kind=song.scores.model.KIND.practice,
                    points__lte=ultimate.points,
                )
                practice_scores.update(is_flagged=True)
                ordered_dsc = song.scores.filter(
                    kind=song.scores.model.KIND.official,
                ).order_by('-points')
                ultimate = ordered_dsc[0]
                penultimate = ordered_dsc[1]
                distance = abs(ultimate.points - penultimate.points)
                try:
                    q = distance / spread
                except ZeroDivisionError:
                    q = 0
                critical = confidence[size]
                if q > critical and ultimate.points - penultimate.points > 5:
                    ultimate.is_flagged = True
                    is_variance = True
                else:
                    ultimate.is_flagged = False
                ultimate.save()
                practice_scores = song.scores.filter(
                    kind=song.scores.model.KIND.practice,
                    points__gte=ultimate.points,
                )
                practice_scores.update(is_flagged=True)
        return is_variance

    # Appearance Permissions
    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_read_permission(self, request):
        return any([
            self.round.status == self.round.STATUS.finished,
            self.round.session.convention.assignments.filter(
                person__user=request.user,
                status__gt=0,
                category__lte=10,
            ),
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
                self.round.session.convention.assignments.filter(
                    person__user=request.user,
                    status__gt=0,
                    category__lte=10,
                ),
                self.round.status != self.round.STATUS.finished,
            ]),
        ])

    # Appearance Conditions
    def can_verify(self):
        try:
            if self.competitor.group.kind == self.competitor.group.KIND.chorus and not self.pos:
                is_pos = False
            else:
                is_pos = True
        except AttributeError:
            is_pos = False
        return all([
            is_pos,
        ])

    # Appearance Transitions
    @fsm_log_by
    @transition(field=status, source=[STATUS.new], target=STATUS.built)
    def build(self, *args, **kwargs):
        Grid = apps.get_model('api.grid')
        Panelist = apps.get_model('api.panelist')
        grid, created = Grid.objects.get_or_create(
            round=self.round,
            num=self.num,
        )
        grid.appearance = self
        grid.save()
        panelists = self.round.panelists.filter(
            category__gt=Panelist.CATEGORY.ca,
        )
        i = 1
        while i <= 2:  # Number songs constant
            song = self.songs.create(
                num=i
            )
            for panelist in panelists:
                song.scores.create(
                    category=panelist.category,
                    kind=panelist.kind,
                    panelist=panelist,
                )
            i += 1
        return

    @fsm_log_by
    @transition(field=status, source=[STATUS.built], target=STATUS.started)
    def start(self, *args, **kwargs):
        self.actual_start = now()
        return

    @fsm_log_by
    @transition(field=status, source=[STATUS.started], target=STATUS.finished)
    def finish(self, *args, **kwargs):
        self.actual_finish = now()
        return

    @fsm_log_by
    @transition(
        field=status,
        source=[STATUS.finished, STATUS.verified, STATUS.variance],
        target=RETURN_VALUE(STATUS.variance, STATUS.verified,),
    )
    def verify(self, *args, **kwargs):
        if self.status == self.STATUS.finished:
            variance = self.check_variance()
            if variance:
                content = self.get_variance()
                self.variance_report.save(
                    "{0}-variance-report".format(
                        slugify(self.competitor.group.name),
                    ),
                    content,
                )
        else:
            variance = None
        return self.STATUS.variance if variance else self.STATUS.verified
