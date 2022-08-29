from rest_framework.serializers import IntegerField, Serializer


class ParsingSerializer(Serializer):
    count = IntegerField()
