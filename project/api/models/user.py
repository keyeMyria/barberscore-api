
# Standard Library
import logging
import uuid

# Third-Party
from auth0.v3.exceptions import Auth0Error
from django_fsm import FSMIntegerField
from django_fsm import transition
from django_fsm_log.decorators import fsm_log_by
from django_fsm_log.decorators import fsm_log_description
from django_fsm_log.models import StateLog
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices

# Django
from django.apps import apps as api_apps
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.functional import cached_property

# First-Party
from api.fields import LowerEmailField
from api.managers import UserManager
from api.tasks import get_auth0

config = api_apps.get_app_config('api')

log = logging.getLogger(__name__)


class User(AbstractBaseUser):
    USERNAME_FIELD = settings.USERNAME_FIELD
    REQUIRED_FIELDS = settings.REQUIRED_FIELDS

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    STATUS = Choices(
        (-10, 'inactive', 'Inactive',),
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
        choices=STATUS,
        default=STATUS.active,
    )

    username = models.CharField(
        max_length=100,
        unique=True,
        editable=True,
    )

    name = models.CharField(
        max_length=100,
        editable=True,
    )

    email = LowerEmailField(
        max_length=100,
        unique=True,
        editable=True,
    )

    bhs_id = models.IntegerField(
        null=True,
        blank=True,
        unique=True,
    )

    current_through = models.DateField(
        null=True,
        blank=True,
        editable=True,
    )

    mc_pk = models.CharField(
        null=True,
        blank=True,
        max_length=36,
        unique=True,
        db_index=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    modified = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    person = models.OneToOneField(
        'Person',
        related_name='user',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    # Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='users',
    )

    objects = UserManager()

    @cached_property
    def is_mc(self):
        """Proxy status."""
        return bool(getattr(getattr(self, 'person'), 'mc_pk', None))

    @cached_property
    def is_active(self):
        """Proxy status."""
        return bool(self.status >= 0)

    @cached_property
    def is_superuser(self):
        return bool(self.is_staff)

    @cached_property
    def is_convention_manager(self):
        return bool(
            self.person.officers.filter(
                office__is_convention_manager=True,
                status__gt=0,
            )
        )

    @cached_property
    def is_session_manager(self):
        return bool(
            self.person.officers.filter(
                office__is_session_manager=True,
                status__gt=0,
            )
        )

    @cached_property
    def is_round_manager(self):
        return bool(
            self.person.officers.filter(
                office__is_round_manager=True,
                status__gt=0,
            )
        )

    @cached_property
    def is_scoring_manager(self):
        return bool(
            self.person.officers.filter(
                office__is_scoring_manager=True,
                status__gt=0,
            )
        )

    @cached_property
    def is_group_manager(self):
        return bool(
            self.person.officers.filter(
                office__is_group_manager=True,
                status__gt=0,
            )
        )

    @cached_property
    def is_person_manager(self):
        return bool(
            self.person.officers.filter(
                office__is_person_manager=True,
                status__gt=0,
            )
        )

    @cached_property
    def is_award_manager(self):
        return bool(
            self.person.officers.filter(
                office__is_award_manager=True,
                status__gt=0,
            )
        )

    @cached_property
    def is_officer_manager(self):
        return bool(
            self.person.officers.filter(
                office__is_officer_manager=True,
                status__gt=0,
            )
        )

    @cached_property
    def is_chart_manager(self):
        return bool(
            self.person.officers.filter(
                office__is_chart_manager=True,
                status__gt=0,
            )
        )

    @cached_property
    def is_assignment_manager(self):
        return bool(
            self.person.officers.filter(
                office__is_assignment_manager=True,
                status__gt=0,
            )
        )

    class JSONAPIMeta:
        resource_name = "user"

    # User Internals
    def __str__(self):
        if self.is_staff:
            return self.name
        if self.bhs_id:
            suffix = "[{0}]".format(self.bhs_id)
        else:
            suffix = "[No BHS ID]"
        full = "{0} {1}".format(
            self.name,
            suffix,
        )
        return " ".join(full.split())

    def clean(self):
        if self.is_staff:
            return
        if not self.person:
            raise ValidationError(
                {'person': 'Non-staff user accounts must have Person attached.'}
            )
        if self.email != self.person.email:
            raise ValidationError(
                {'email': 'Email does not match person'}
            )
        if self.name != self.person.common_name:
            raise ValidationError(
                {'name': 'Name does not match person'}
            )
        if self.bhs_id != self.person.bhs_id:
            raise ValidationError(
                {'bhs_id': 'BHS ID does not match person'}
            )

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    # Methods
    def update_or_create_account(self):
        if self.is_staff:
            raise ValueError('Staff should not have accounts')
        auth0 = get_auth0()
        email = self.email.lower()
        pk = str(self.id)
        status = self.get_status_display()
        name = self.name.strip()
        bhs_id = self.bhs_id
        if self.current_through:
            current_through = self.current_through.isoformat()
        else:
            current_through = None
        payload = {
            'email': email,
            'email_verified': True,
            'app_metadata': {
                'pk': pk,
                'status': status,
                'name': name,
                'bhs_id': bhs_id,
                'current_through': current_through,
            }
        }
        if self.username.startswith('auth0|'):
            account = auth0.users.update(self.username, payload)
            created = False
        elif self.username.startswith('orphan|'):
            payload['connection'] = 'Default'
            payload['password'] = get_random_string()
            try:
                account = auth0.users.create(payload)
            except Auth0Error as e:
                if e.message == 'The user already exists.':
                    accounts = auth0.users_by_email.search_users_by_email(self.email)
                    account = accounts[0]
                    self.username = account['user_id']
                    self.save()
                    created = False
                    return account, created
                raise(e)
            created = True
        else:
            ValueError("Unknown Username type")
        return account, created

    def delete_account(self):
        auth0 = get_auth0()
        # Delete Auth0
        result = auth0.users.delete(self.username)
        return result

    def get_or_create_person(self):
        Person = apps.get_model('api.person')
        auth0 = get_auth0()
        account = auth0.users.get(self.username)
        email = account['email'].lower()
        person, created = Person.objects.get_or_create(email=email)
        return person, created

    def unlink_user_account(self):
        client = get_auth0()
        user_id = self.username.partition('|')[2]
        client.users.unlink_user_account(
            self.account_id,
            'auth0',
            user_id,
        )
        return

    def relink_user_account(self):
        client = get_auth0()
        user_id = self.account_id.partition('|')[2]
        payload = {
            'provider': 'email',
            'user_id': user_id,
        }
        client.users.link_user_account(
            self.username,
            payload,
        )
        return


    # User Permissions
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
        return True

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        if request.user == self:
            return True
        return False

    # User Transitions
    @fsm_log_by
    @fsm_log_description
    @transition(field=status, source='*', target=STATUS.active)
    def activate(self, description=None, *args, **kwargs):
        # Should deactive AUTH0
        return

    @fsm_log_by
    @fsm_log_description
    @transition(field=status, source='*', target=STATUS.inactive)
    def deactivate(self, description=None, *args, **kwargs):
        # Should deactive AUTH0
        return
