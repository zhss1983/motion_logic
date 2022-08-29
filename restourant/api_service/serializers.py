from rest_framework.serializers import ModelSerializer, SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from .models import ObjectType, Organisation, Owner, Phone


class ObjectTypeSerializer(ModelSerializer):
    class Meta:
        model = ObjectType
        fields = ("pk", "title")


class OrganisationSerializer(ModelSerializer):
    object_type = SlugRelatedField(slug_field="title", queryset=ObjectType.objects.all())

    class Meta:
        UNIQUE_ERROR = "Две организации с одним и тем же названием не могут находиться по одному и тому же адресу."
        model = Organisation
        fields = ("pk", "title", "object_type", "address", "latitude", "longitude", "description")
        validators = (
            UniqueTogetherValidator(
                queryset=Organisation.objects.all(),
                fields=("title", "address"),
                message=UNIQUE_ERROR,
            ),
        )


class PhoneSerializer(ModelSerializer):
    organisation = SlugRelatedField(slug_field="title", queryset=Organisation.objects.all())  # , read_only=True

    class Meta:
        model = Phone
        fields = ("pk", "phone", "organisation")


class OwnerSerializer(ModelSerializer):
    organisation = SlugRelatedField(slug_field="title", queryset=Organisation.objects.all())
    owner = SlugRelatedField(slug_field="title", queryset=Organisation.objects.all())

    class Meta:
        model = Owner
        fields = ("pk", "organisation", "owner")
