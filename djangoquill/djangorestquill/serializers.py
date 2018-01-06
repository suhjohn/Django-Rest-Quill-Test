from django.db.transaction import atomic
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from djangorestquill.models import QuillPost, DeltaOperation
from djangorestquill.quill_js import DjangoQuill

django_quill = DjangoQuill(model=DeltaOperation)

class QuillRelatedPostModelSerializer(serializers.ModelSerializer):
    PREVIEW_LENGTH = 200

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
        quillpost = quillserializer.save(preview_length=self.PREVIEW_LENGTH)
        object = self.Meta.model.objects.create(quillpost=quillpost, **validated_data)
        return object


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
        """
        Validate content and content_html

        :param attrs:
        :return:
        """
        return attrs

    def save(self, preview_length=200, **kwargs):
        """

        :param kwargs:
        :return:
        """
        content, content_html = self.validated_data.pop('content', None), self.validated_data.pop('content_html', None)
        post = QuillPost.objects.create()

        # request_user를 **kwargs에 추가하여 super().save() 호출
        with atomic():
            django_quill.post = post
            self._save_delta_operations(content=content)
            if content_html:
                self._save_content_html(content_html=content_html, post=post, preview_length=preview_length)
        return post

    def _save_delta_operations(self, content):
        """

        :param content:
        :param answer_instance:
        :return:
        """
        instances = django_quill.get_delta_operation_instances(content=content)
        try:
            DeltaOperation.objects.bulk_create(instances)
        except:
            raise ParseError({"error": "Delta Operation을 저장하는데 문제가 있었습니다."})

    def _save_content_html(self, content_html, post, preview_length):
        """
        html 업데이트

        :param content_html:
        :return:
        """
        img_delta_objs = post.delta_operation_set.exclude(image='').order_by('line_no')
        html = django_quill.replace_image_64(objs=img_delta_objs, html=content_html)
        preview_html = django_quill.get_html_preview(html=html, preview_len=preview_length)
        QuillPost.objects.filter(pk=post.pk).update(content_html=html, content_preview_html=preview_html)
        post.content_html, post.content_preview_html = html, preview_html
