from rest_framework import generics

from answer.models import Answer
from answer.serializers import AnswerSerializer


class AnswerListCreateAPI(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class AnswerRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
