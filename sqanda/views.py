from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from .models import Question
from rest_framework import serializers, status
from rest_framework.response import Response


class QuestionViewSet(APIView):
    class QuestionViewSerializer(serializers.ModelSerializer):
        class Meta:
            model = Question
            fields = ('id', 'get_kb_base', 'get_kb_category', 'get_kb_knowledge', 'question', 'question_details',
                      'get_created_by', )

    def get(self, request, base, category, knowledge, format=None):

        return Response('', status=status.HTTP_200_OK)

    def post(self, request, format=None):
        if request.user.is_anonymous:
            return Response('', status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response('', status=status.HTTP_201_CREATED)

