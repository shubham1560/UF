import binascii
import os
import json

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
                      'get_created_by', 'get_updated_by', 'sys_created_on', 'sys_updated_on', 'question_url')

    def get(self, request, format=None):
        kb_category = request.query_params.get('path')
        kb_base = request.query_params.get('root')
        kb_knowledge = request.query_params.get('article')
        start = int(request.query_params.get('start'))
        end = int(request.query_params.get('end'))
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
        # breakpoint()
        if request.user.is_anonymous:
            return Response('', status=status.HTTP_401_UNAUTHORIZED)
        else:
            question = Question()
            question.question = request.data['question']
            question.question_details = request.data['description']
            try:
                question.kb_category = KbCategory.objects.get(id=request.data['path'])
            except ObjectDoesNotExist:
                pass
            try:
                question.kb_base = KbKnowledgeBase.objects.get(id=request.data['root'])
            except ObjectDoesNotExist:
                pass
            question.sys_created_by = request.user
            question.id = binascii.hexlify(os.urandom(3)).decode()
            question.question_url = request.data['question'].lower().replace(" ", "-")
            question.save()
            return Response('', status=status.HTTP_201_CREATED)


class GetQuestionAndAnswer(APIView):
    class QuestionViewSerializer(serializers.ModelSerializer):
        class Meta:
            model = Question
            fields = ('id', 'get_kb_base', 'get_kb_category', 'get_kb_knowledge', 'question', 'question_details',
                      'get_created_by', 'get_updated_by', 'sys_created_on', 'sys_updated_on')

    def get(self, request, question_id, format=None):
        question = Question.objects.get(id=question_id)
        # breakpoint()
        # question_details = json.loads(question.question_details)
        result = self.QuestionViewSerializer(question)
        # response = {"result": result.data, "question_detail": question_details}
        return Response(result.data, status=status.HTTP_200_OK)

