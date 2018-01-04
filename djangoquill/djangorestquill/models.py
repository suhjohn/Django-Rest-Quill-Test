from bs4 import BeautifulSoup
from django.contrib.postgres.fields import JSONField
from django.db import models

from djangorestquill.quill_js import DjangoQuill

__all__ = (
    'Answer',
    'DeltaOperation',
)


class Post(models.Model):
    content_html = models.TextField(null=True, blank=True)
    content_preview_html = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.text_content[:30]}...'

    @property
    def content(self):
        """
        Answer와 연결된 QuillDeltaOperation set을 가지고 와서 quillJS delta 형태로 반환
        :return:
        """
        quill_delta_operation_querydict = self.quill_delta_operation_set.all().order_by('line_no')
        if not quill_delta_operation_querydict:
            return ""
        delta_operation_list = list()
        for quill_delta_operation in quill_delta_operation_querydict:
            delta_operation_list.append(quill_delta_operation.delta_operation)

        content = DjangoQuill.create_quill_content(delta_operation_list=delta_operation_list)
        return content

    @property
    def text_content(self):
        """
        Answer과 연결된 QuillDeltaOperation set 중 insert_value만 parse해서 반환
        :return:
        """
        soup = BeautifulSoup(self.content_html, 'html.parser')
        return soup.get_text()


class DeltaOperation(models.Model):
    """
    QuillJS 의 Content중 Operation 한 줄에 대한 정보를 갖는 모델
    해당 content가 쓰인 Post와 ForeignKey로 연결이 되어 있음
    """
    line_no = models.IntegerField(null=False)

    insert_value = models.TextField(null=True, blank=True)
    image_insert_value = JSONField(null=True, blank=True)
    video_insert_value = JSONField(null=True, blank=True)
    attributes_value = JSONField(null=True, blank=True)

    image = models.ImageField(null=True, blank=True, upload_to='answer')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='quill_delta_operation_set')

    def __str__(self):
        return f'{self.delta_operation}'

    @property
    def delta_operation(self):
        """
        quill의 operation 하나를 반환
        text 일 경우
        { insert: 'Gandalf', attributes: { bold: true } }

        image 일 경우
        { insert: { image: 'https://octodex.github.com/images/labtocat.png' }}

        :return: quill delta operation
        """
        quill_delta_operation = dict()
        if self.attributes_value:
            quill_delta_operation['attributes'] = self.attributes_value
        if self.insert_value:
            quill_delta_operation['insert'] = self.insert_value
        elif self.image_insert_value:
            quill_delta_operation['insert'] = self.image_insert_value
        elif self.video_insert_value:
            quill_delta_operation['insert'] = self.video_insert_value
        else:
            raise AssertionError(
                "Neither 'text' or 'image' in answer_content. This is an empty instance and should be deleted.")
        return quill_delta_operation

    def delete(self, *args, **kwargs):
        """
        Delta Operation 삭제 시 이미지가 있을 경우 storage에 있는 이미지도 삭제

        :param args:
        :param kwargs:
        :return:
        """
        if self.image:
            storage, path = self.image.storage, self.image.path
            storage.delete(path)
        super().delete(*args, **kwargs)
