# Standard Libary
import logging

# Third-Party
from django_filters.rest_framework import DjangoFilterBackend
# from dry_rest_permissions.generics import DRYPermissions
from rest_framework import (
    # status,
    viewsets,
)
# from rest_framework.decorators import (
#     detail_route,
#     parser_classes,
# )
# from rest_framework.parsers import (
#     FormParser,
#     MultiPartParser,
# )
from rest_framework.permissions import (
    AllowAny,
)
# from rest_framework.response import Response
# from rest_framework_csv.renderers import CSVRenderer

# Local
# from .backends import (
#     CoalesceFilterBackend,
# )
# from .filters import (
# )
from .models import (
    Human,
    Structure,
)
from .serializers import (
    HumanSerializer,
    StructureSerializer,
)

log = logging.getLogger(__name__)


class HumanViewSet(viewsets.ModelViewSet):
    queryset = Human.objects.select_related(
    ).prefetch_related(
    ).order_by('last_name', 'first_name')
    serializer_class = HumanSerializer
    filter_class = None
    filter_backends = [
        # CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    permission_classes = [
        AllowAny,
    ]
    resource_name = "human"


class StructureViewSet(viewsets.ModelViewSet):
    queryset = Structure.objects.select_related(
    ).prefetch_related(
    ).order_by('name',)
    serializer_class = StructureSerializer
    filter_class = None
    filter_backends = [
        # CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    permission_classes = [
        AllowAny,
    ]
    resource_name = "structure"