from rest_framework import serializers

from answer.models import Answer
from djangorestquill.models import QuillPost
from djangorestquill.serializers import QuillPostSerializer


class AnswerSerializer(serializers.ModelSerializer):
    quill_content = QuillPostSerializer()

    class Meta:
        model = Answer
        fields = (
            'id',
            'title',
            'quill_content'
        )

    # def create(self, validated_data):
    #     tracks_data = validated_data.pop('tracks')
    #     album = Album.objects.create(**validated_data)
    #     for track_data in tracks_data:
    #         Track.objects.create(album=album, **track_data)
    #     return album


    def create(self, validated_data):
        quill_content = validated_data.pop('quill_content')
        quillpost = QuillPostSerializer(**quill_content)
        object = self.Meta.model.objects.create(quillpost=quillpost, **validated_data)
        return object

