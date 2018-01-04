from rest_framework import serializers

from djangorestquill.models import QuillPost


class QuillPostSerializer(serializers.ModelSerializer):
    content = serializers.JSONField(default=None)

    class Meta:
        model = QuillPost
        fields = (
            'content_html',
            'content_preview_html',
            'content',
        )


    def validate(self, attrs):
        print("------QuillPostSerializer Validate--------")
        print(self.__dict__)
        print(attrs)
        return attrs


    def save(self, **kwargs):
        print(self.data)
        pass
