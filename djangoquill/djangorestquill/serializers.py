from django.db.transaction import atomic
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from djangorestquill.models import QuillPost, DeltaOperation
from djangorestquill.quill_js import DjangoQuill

django_quill = DjangoQuill(model=DeltaOperation)


class QuillPostSerializer(serializers.Serializer):
    content = serializers.JSONField(default=None)
    content_html = serializers.CharField(max_length=10000, required=False)
    content_preview_html = serializers.CharField(max_length=10000, required=False)

    class Meta:
        model = QuillPost
        fields = (
            'content_html',
            'content_preview_html',
            'content',
        )

    def validate(self, attrs):
        return attrs

    def save(self, preview_length, **kwargs):
        """
        Answer 객체를 만들고 content를 AnswerContent로 변환하여 저장
        :param kwargs:
        :return:
        """
        content = self.validated_data.pop('content', None)
        content_html = self.validated_data.pop('content_html', None)
        post = QuillPost.objects.create()

        # request_user를 **kwargs에 추가하여 super().save() 호출
        with atomic():
            self._save_quill_delta_operation(content=content, post=post)
            if content_html:
                self._save_content_html(content_html=content_html, post=post, preview_length=preview_length)
        return post

    def _save_quill_delta_operation(self, content, post):
        """

        :param content:
        :param answer_instance:
        :return:
        """
        instances = django_quill.get_delta_operation_instances(
            content=content,
            post=post,
        )
        if not instances:
            raise ParseError({"error": "content가 잘못된 포맷입니다. "})
        # try:
        DeltaOperation.objects.bulk_create(instances)
        # except:
        #     raise ParseError({"error": "Delta Operation을 저장하는데 문제가 있었습니다."})

    def _save_content_html(self, content_html, post, preview_length=200):
        """
        html 업데이트
        :param content_html:
        :return:
        """
        img_delta_objs = self.instance.quill_delta_operation_set.exclude(image='').order_by('line_no')
        html = django_quill.img_base64_to_link(
            objs=img_delta_objs,
            html=content_html
        )
        preview_html = django_quill.html_preview_parse(html=html, preview_len=preview_length)
        # Django Bug - Updating an instance during save method will not result in a properly serialized object
        post.update(content_html=html, content_html_preview=preview_html)
