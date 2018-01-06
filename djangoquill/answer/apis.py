from rest_framework import generics, status
from rest_framework.response import Response

from answer.models import Answer
from answer.serializers import AnswerSerializer


class AnswerListCreateAPI(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

class AnswerRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AnswerSerializer
