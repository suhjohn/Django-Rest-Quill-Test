from rest_framework import serializers


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        fields = __all__
