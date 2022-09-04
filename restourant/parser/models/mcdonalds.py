from rest_framework.serializers import BooleanField, CharField, FloatField, IntegerField, ListField, Serializer

from ..constants import MAX_METRO_DISTANT


class McDonaldsMetroSerializer(Serializer):
    name = CharField(default="", allow_blank=True)
    dist = IntegerField(default=MAX_METRO_DISTANT, min_value=0)


class McDonaldsFeaturesSerializer(Serializer):
    name = CharField(default="", allow_blank=True, required=False)


class McDonaldsRestaurantSerializer(Serializer):
    name = CharField()
    address = CharField()
    phone = CharField(default="", allow_blank=True)
    features = ListField(child=McDonaldsFeaturesSerializer())


class McDonaldsSerializer(Serializer):
    metro = ListField(child=McDonaldsMetroSerializer())
    restaurant = McDonaldsRestaurantSerializer()
    message = CharField(default="", allow_blank=True)
