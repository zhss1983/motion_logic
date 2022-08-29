from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from .models import ObjectType, Organisation, Owner, Phone
from .serializers import (
    ObjectTypeSerializer,
    OrganisationByOwnerSerializer,
    OrganisationSerializer,
    OwnerSerializer,
    PhoneSerializer,
)


class PhoneViewSet(ModelViewSet):
    serializer_class = PhoneSerializer
    queryset = Phone.objects.all()


class OwnerViewSet(ModelViewSet):
    serializer_class = OwnerSerializer
    queryset = Owner.objects.all()


class ObjectTypeViewSet(ModelViewSet):
    serializer_class = ObjectTypeSerializer
    queryset = ObjectType.objects.all()


class OrganisationViewSet(ModelViewSet):
    serializer_class = OrganisationSerializer
    queryset = Organisation.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["=title", "address"]


class OrganisationByOwnerViewSet(ModelViewSet):
    serializer_class = OrganisationByOwnerSerializer
    queryset = Owner.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["=owner__title"]
