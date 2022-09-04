from rest_framework.serializers import BooleanField, CharField, FloatField, Serializer


class BurgerKingSerializer(Serializer):
    address = CharField(allow_blank=True)
    latitude = FloatField(default=0, min_value=0, max_value=360)
    longitude = FloatField(default=0, min_value=0, max_value=360)
    phone = CharField(allow_blank=True)
    name = CharField(allow_blank=True)
    breakfast = BooleanField(default=False, required=False)
    children_party = BooleanField(default=False, required=False)
    metro = CharField(allow_blank=True, allow_null=True, required=False)
    king_drive = BooleanField(default=False, required=False)
    parking_delivery = BooleanField(default=False, required=False)
    table_delivery = BooleanField(default=False, required=False)
    wifi = BooleanField(default=False, required=False)


class BurgerKingSearchResultsSerializer(Serializer):
    items = BurgerKingSerializer(many=True)
