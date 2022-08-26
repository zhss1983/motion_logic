from .serializers import PhoneSerializer, OrganisationSerializer, ObjectTypeSerializer
from django.shortcuts import get_object_or_404

from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from .models import Phone, ObjectType, Organisation


class PhoneViewSet(ModelViewSet):
    serializer_class = PhoneSerializer
    queryset = Phone.objects.all()


class ObjectTypeViewSet(ModelViewSet):
    serializer_class = ObjectTypeSerializer
    queryset = ObjectType.objects.all()


class OrganisationViewSet(ModelViewSet):
    serializer_class = OrganisationSerializer
    queryset = Organisation.objects.all()
