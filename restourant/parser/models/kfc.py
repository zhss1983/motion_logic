from rest_framework.serializers import CharField, FloatField, ListField, Serializer


class KFCGeometrySerializer(Serializer):
    coordinates = ListField(child=FloatField(default=0, min_value=0, max_value=360), min_length=2, max_length=2)


class KFCEnRuStatementSerializer(Serializer):
    en = CharField(default="", allow_blank=True)
    ru = CharField(default="", allow_blank=True, required=False)


class KFCCoordinatesContactsSerializer(Serializer):
    geometry = KFCGeometrySerializer()


class KFCContactsSerializer(Serializer):
    coordinates = KFCCoordinatesContactsSerializer()
    phoneNumber = CharField(default="", allow_blank=True, required=False)
    streetAddress = KFCEnRuStatementSerializer()


class KFCStoreSerializer(Serializer):
    contacts = KFCContactsSerializer()
    features = ListField(child=CharField(default="", allow_blank=True), allow_empty=True)
    title = KFCEnRuStatementSerializer()


class KFCSerializer(Serializer):
    distanceMeters = FloatField(allow_null=True, default=None, required=False)
    store = KFCStoreSerializer()


class KFCSearchResultsSerializer(Serializer):
    searchResults = KFCSerializer(many=True)
