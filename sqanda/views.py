from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from knowledge.models import KbKnowledgeBase, KbCategory, KbKnowledge
from .models import Question
from rest_framework import serializers, status
from rest_framework.response import Response


class QuestionViewSet(APIView):
    class QuestionViewSerializer(serializers.ModelSerializer):
        class Meta:
            model = Question
            fields = ('id', 'get_kb_base', 'get_kb_category', 'get_kb_knowledge', 'question', 'question_details',
                      'get_created_by', 'get_updated_by', 'sys_created_on', 'sys_updated_on')

    def get(self, request, format=None):
        # breakpoint()
        kb_category = request.query_params.get('path')
        kb_base = request.query_params.get('root')
        kb_knowledge = request.query_params.get('article')
        start = int(request.query_params.get('start'))
        end = int(request.query_params.get('end'))
        # breakpoint()
        if kb_knowledge != 'null':
            try:
                kb_knowledge = KbKnowledge.objects.get(id=kb_knowledge)
                questions = Question.objects.filter(kb_knowledge=kb_knowledge)[start:end]
            except ObjectDoesNotExist:
                questions = Question.objects.all()
        elif kb_category != 'null':
            try:
                kb_category = KbCategory.objects.get(id=kb_category)
                questions = Question.objects.filter(kb_category=kb_category)[start:end]
            except ObjectDoesNotExist:
                questions = Question.objects.all()

        elif kb_base != 'null':
            try:
                kb_base = KbKnowledgeBase.objects.get(id=kb_base)
                questions = Question.objects.filter(kb_base=kb_base)[start:end]
            except ObjectDoesNotExist:
                questions = Question.objects.all()[start:end]
        else:
            questions = Question.objects.all()[start:end]
        result = self.QuestionViewSerializer(questions, many=True)
        return Response(result.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        if request.user.is_anonymous:
            return Response('', status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response('', status=status.HTTP_201_CREATED)

