from rest_framework.serializers import IntegerField, ModelSerializer, Serializer


class ParsingSerializer(Serializer):
    count = IntegerField()
