from rest_framework import serializers

from answer.models import Answer
from djangorestquill.models import QuillPost
from djangorestquill.serializers import QuillPostSerializer, QuillRelatedPostModelSerializer


class AnswerSerializer(QuillRelatedPostModelSerializer):
    quillpost = QuillPostSerializer()

    PREVIEW_LENGTH = 12
    class Meta:
        model = Answer
        fields = (
            'id',
            'title',
            'quillpost',
        )


