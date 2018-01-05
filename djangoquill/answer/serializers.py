from rest_framework import serializers

from answer.models import Answer
from djangorestquill.models import QuillPost
from djangorestquill.serializers import QuillPostSerializer


class AnswerSerializer(serializers.ModelSerializer):
    quillpost = QuillPostSerializer()

    class Meta:
        model = Answer
        fields = (
            'id',
            'title',
            'quillpost',
        )

    def create(self, validated_data):
        """
        Override Create method for QuillPost creation.
        Pass in possible argument preview_length to save()
        :param validated_data:
        :return:
        """
        quillpost = validated_data.pop('quillpost')
        quillserializer = QuillPostSerializer(data=quillpost)
        quillserializer.is_valid()
        quillpost = quillserializer.save(preview_length=200)
        object = self.Meta.model.objects.create(quillpost=quillpost, **validated_data)
        return object

