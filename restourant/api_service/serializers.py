from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from .models import Phone, Organisation, ObjectType


class ObjectTypeSerializer(ModelSerializer):
    class Meta:
        model = ObjectType
        fields = ('pk', 'title')


class OrganisationSerializer(ModelSerializer):
    object_type = SlugRelatedField(slug_field='title', read_only=True)
    class Meta:
        UNIQUE_ERROR = 'Две организации с одним и тем же названием не могут находиться по одному и тому же адресу.'
        model = Organisation
        fields = ('pk', 'title', 'object_type', 'address', 'description')
        validators = (
            UniqueTogetherValidator(
                queryset=Organisation.objects.all(),
                fields=('title', 'address'),
                message=UNIQUE_ERROR
            ),
        )



class PhoneSerializer(ModelSerializer):
    organisation = SlugRelatedField(slug_field='title', read_only=True)
    class Meta:
        model = Phone
        fields = ('phone', 'organisation')
