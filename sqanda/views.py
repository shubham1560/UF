import binascii
import os
import json

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from knowledge.models import KbKnowledgeBase, KbCategory, KbKnowledge
from .models import Question, Comment, Answer
from rest_framework import serializers, status
from rest_framework.response import Response
from .services import get_answers_question, editor_service, get_questions_base_category, post_question_base_category, \
    post_answer, post_comment


class QuestionViewSet(APIView):
    class QuestionViewSerializer(serializers.ModelSerializer):
        class Meta:
            model = Question
            fields = ('id', 'get_kb_base', 'get_kb_category', 'get_kb_knowledge', 'question', 'question_details',
                      'get_created_by', 'get_updated_by', 'sys_created_on', 'sys_updated_on', 'question_url',
                      'update_count')

    def get(self, request, format=None):
        questions = get_questions_base_category(request)
        result = self.QuestionViewSerializer(questions, many=True)
        return Response(result.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        response = post_question_base_category(request)
        return Response(response["message"], status=response["status"])


class GetQuestionAndAnswer(APIView):
    class QuestionViewSerializer(serializers.ModelSerializer):
        class Meta:
            model = Question
            fields = ('id', 'get_kb_base', 'get_kb_category', 'get_kb_knowledge', 'question', 'question_details',
                      'get_created_by', 'get_updated_by', 'sys_created_on', 'sys_updated_on', 'update_count')

    class CommentSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = ('id', 'comment', 'get_created_by', 'sys_created_on', 'sys_updated_on')

    def get(self, request, question_id, format=None):
        question = Question.objects.get(id=question_id)
        comments = Comment.objects.filter(table_id=question.id, table_name="question").order_by('-sys_created_on')
        comm = self.CommentSerializer(comments, many=True)
        answers = get_answers_question(question_id, request)
        question_owner = False
        if question.sys_created_by == request.user:
            question_owner = True
        result = self.QuestionViewSerializer(question)
        return Response({'question': result.data, 'comments': comm.data, 'question_owner': question_owner,
                         'answers': answers},
                        status=status.HTTP_200_OK)


class CommentViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    class CommentSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = ('id', 'comment', 'get_created_by', 'sys_created_on', 'sys_updated_on')

    def post(self, request, format=None):
        comment = post_comment(request)
        result = self.CommentSerializer(comment, many=False)
        return Response(result.data, status=status.HTTP_201_CREATED)


class EditorDataViewSet(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, format=None):
        response = editor_service(request)
        return Response(response['message'], status=response['status'])


class AnswersQuestion(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, format=None):
        response = post_answer(request)
        return Response(response["message"], status=response["status"])



