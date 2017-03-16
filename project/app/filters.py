# Third-Party
from django_filters.rest_framework import FilterSet

# Local
from .models import (
    Award,
    Catalog,
    Contestant,
    Convention,
    Entity,
    Officer,
    Performer,
    Person,
    Session,
    Submission,
    Venue,
)


class AwardFilter(FilterSet):
    class Meta:
        model = Award
        fields = {
            'nomen': [
                'icontains',
            ],
            'entity__hosts__convention': [
                'exact',
            ],
        }


class CatalogFilter(FilterSet):
    class Meta:
        model = Catalog
        fields = {
            'nomen': [
                'icontains',
            ],
        }


class ContestantFilter(FilterSet):
    class Meta:
        model = Contestant
        fields = {
            'nomen': [
                'icontains',
            ],
        }


class ConventionFilter(FilterSet):
    class Meta:
        model = Convention
        fields = {
            'status': [
                'exact',
                'lt',
            ],
            'year': [
                'exact',
            ],
            'assignments__person__user': [
                'exact',
            ],
            'assignments__kind': [
                'exact',
            ],
            'entity__memberships__officers': [
                'exact',
            ],
        }


class EntityFilter(FilterSet):
    class Meta:
        model = Entity
        fields = {
            'kind': [
                'exact',
                'lt',
                'in',
            ],
            'parent': [
                'exact',
            ],
            'nomen': [
                'icontains',
            ],
            'status': [
                'exact',
                'gt',
            ],
            'memberships__person__user': [
                'exact',
            ],
        }


class OfficerFilter(FilterSet):
    class Meta:
        model = Officer
        fields = {
            'membership__person__user': [
                'exact',
            ],
            'office__short_name': [
                'exact',
            ],
        }


class PerformerFilter(FilterSet):
    class Meta:
        model = Performer
        fields = {
            'nomen': [
                'icontains',
            ],
            'entity__memberships__person__user': [
                'exact',
            ],
        }


class PersonFilter(FilterSet):
    class Meta:
        model = Person
        fields = {
            'nomen': [
                'icontains',
            ],
            'status': [
                'exact',
            ],
            'user': [
                'exact',
            ],
            'memberships__officers__office__kind': [
                'exact',
            ],
        }


class SessionFilter(FilterSet):
    class Meta:
        model = Session
        fields = {
            'status': [
                'exact',
            ],
            'convention': [
                'exact',
            ],
            'nomen': [
                'icontains',
            ],
            'convention__assignments__person__user': [
                'exact',
            ],
            'convention__assignments__kind': [
                'exact',
            ],
        }


class SubmissionFilter(FilterSet):
    class Meta:
        model = Submission
        fields = {
            'status': [
                'exact',
            ],
        }


class VenueFilter(FilterSet):
    class Meta:
        model = Venue
        fields = {
            'nomen': [
                'icontains',
            ],
        }
