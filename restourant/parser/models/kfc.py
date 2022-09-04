from rest_framework.serializers import BooleanField, CharField, FloatField, IntegerField, ListField, Serializer

from ..constants import MAX_METRO_DISTANT


class KFCGeometrySerializer(Serializer):
    coordinates: list[float, float] = [0.0, 0.0]


class KFCEnRuStatementSerializer(Serializer):
    en = CharField(default="", allow_blank=True, required=False)
    ru = CharField(default="", allow_blank=True, required=False)


class KFCCoordinatesContactsSerializer(Serializer):
    geometry: KFCGeometrySerializer()


class KFCContactsSerializer(Serializer):
    coordinates = KFCCoordinatesContactsSerializer()
    phoneNumber = CharField(default="", allow_blank=True, required=False)
    streetAddress = KFCEnRuStatementSerializer


class KFCStoreSerializer(Serializer):
    contacts = KFCContactsSerializer()
    features = ListField(child=CharField(default="", allow_blank=True), allow_empty=True)
    title = KFCEnRuStatementSerializer()


class KFCSerializer(Serializer):
    distanceMeters = IntegerField(allow_null=True, default=MAX_METRO_DISTANT, required=False)
    store = KFCStoreSerializer()


class KFCSearchResultsSerializer(Serializer):
    searchResults = KFCSerializer(many=True)
