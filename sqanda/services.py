import binascii
import os

from django.core.exceptions import ObjectDoesNotExist

from .models import Answer, Question, Comment
from rest_framework import status
from knowledge.models import KbCategory, KbKnowledge, KbKnowledgeBase


def get_questions_base_category(request):
    kb_category = request.query_params.get('path')
    kb_base = request.query_params.get('root')
    kb_knowledge = request.query_params.get('article')
    start = int(request.query_params.get('start'))
    end = int(request.query_params.get('end'))
    if kb_knowledge != 'null':
        try:
            kb_knowledge = KbKnowledge.objects.get(id=kb_knowledge)
            questions = Question.objects.filter(kb_knowledge=kb_knowledge).order_by('-sys_updated_on')[start:end]
        except ObjectDoesNotExist:
            questions = Question.objects.all()
    elif kb_category != 'null':
        try:
            kb_category = KbCategory.objects.get(id=kb_category)
            questions = Question.objects.filter(kb_category=kb_category).order_by('-sys_updated_on')[start:end]
        except ObjectDoesNotExist:
            questions = Question.objects.all()

    elif kb_base != 'null':
        try:
            kb_base = KbKnowledgeBase.objects.get(id=kb_base)
            questions = Question.objects.filter(kb_base=kb_base).order_by('-sys_updated_on')[start:end]
        except ObjectDoesNotExist:
            questions = Question.objects.all()[start:end]
    else:
        questions = Question.objects.all().order_by('-sys_updated_on')[start:end]
    return questions


def post_question_base_category(request):
    if request.user.is_anonymous:
        response = {"message": '', "status": status.HTTP_401_UNAUTHORIZED}
        # return Response('', status=status.HTTP_401_UNAUTHORIZED)
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
        question_detail = {"question_id": question.id, "question_title": question.question_url}
        response = {"message": question_detail, "status": status.HTTP_201_CREATED}
    return response


def get_answers_question(question_id, request):
    question = Question.objects.get(id=question_id)
    answers = Answer.objects.select_related('sys_created_by').filter(question=question).order_by('-sys_created_on')
    answers_dict_array = []
    for answer in answers:
        if answer.sys_created_by.public and answer.sys_created_by.is_active:
            sys_created_by = {
                "name": answer.sys_created_by.first_name + " " + answer.sys_created_by.last_name,
                'id': answer.sys_created_by.id_name,
                # "username": answer.sys_created_by.username
            }
        else:
            sys_created_by = {
            }
        ans = {
            "id": answer.id,
            "owner": False,
            "answer": answer.answer,
            "sys_created_by":
                sys_created_by
            ,
            "sys_created_on": answer.sys_created_on,
            "update_count": answer.update_count,
            "sys_updated_on": answer.sys_updated_on,
            "comments": [
            ]
        }

        if answer.sys_created_by == request.user:
            ans["owner"] = True
        comments = Comment.objects.select_related('sys_created_by').filter(table_id=answer.id, table_name="answer")
        for comment in comments:
            if comment.sys_created_by.public and answer.sys_created_by.is_active:
                sys_created_by = {
                    "name": comment.sys_created_by.first_name + " " + comment.sys_created_by.last_name,
                    'id': comment.sys_created_by.id_name,
                    # "username": comment.sys_created_by.username
                }
            else:
                sys_created_by = {
                }
            comm = {
                "id": comment.id,
                "owner": False,
                "sys_created_by":
                    sys_created_by
                ,
                "sys_created_on": comment.sys_updated_on,

                "comment": comment.comment
            }
            ans["comments"].append(comm)
        answers_dict_array.append(ans)
    return answers_dict_array


def editor_service(request):
    response = {"message": "", "status": status.HTTP_200_OK}
    table_id = request.data['table_id']
    table_name = request.data['table_name']
    editor_data = request.data['editor_data']
    if table_name == 'question':
        try:
            record = Question.objects.get(id=table_id)
        except ObjectDoesNotExist:
            response = {"message": "Not Found!", "status": status.HTTP_404_NOT_FOUND}
            return response
        record.question_details = editor_data

    elif table_name == 'answer':
        try:
            record = Answer.objects.get(id=table_id)
        except ObjectDoesNotExist:
            response = {"message": "Not Found!", "status": status.HTTP_404_NOT_FOUND}
            return response
        record.answer = editor_data
    if record.sys_created_by != request.user:
        response["message"] = 'unauthorized! the record is not yours'
        response["status"] = status.HTTP_401_UNAUTHORIZED
        return response
        # return Response('unauthorized! the question is not yours', status=status.HTTP_401_UNAUTHORIZED)
    record.update_count += 1
    record.save()
    response = {"message": "success", "status": status.HTTP_201_CREATED}
    return response


def post_answer(request):
    try:
        question = Question.objects.get(id=request.data['question'])
    except ObjectDoesNotExist:
        response = {"message": "", 'status': status.HTTP_404_NOT_FOUND}
        return response
    answer = Answer()
    answer.id = binascii.hexlify(os.urandom(3)).decode()
    answer.answer = request.data['description']
    answer.sys_created_by = request.user
    answer.question = question
    answer.save()
    response = {
        "id": answer.id,
        "owner": True,
        "answer": request.data['description'],
        "sys_created_by": {
            "name": request.user.first_name + " " + request.user.last_name,
            "id": request.user.id_name,
        },
        "sys_created_on": answer.sys_updated_on,
        'comments': [

        ]
    }
    response = {"message": response, "status": status.HTTP_201_CREATED}
    return response


def post_comment(request):
    comment = Comment()
    comment.table_id = request.data['table_id']
    comment.table_name = request.data['table_name']
    comment.comment = request.data['comment']
    comment.sys_created_by = request.user
    comment.save()
    return comment
