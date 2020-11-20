from .models import Answer, Question, Comment


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
            "owner": False,
            "answer": answer.answer,
            "sys_created_by":
                sys_created_by
            ,
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
                "owner": False,
                "sys_created_by":
                    sys_created_by
                ,
                "comment": comment.comment
            }
            ans["comments"].append(comm)
        answers_dict_array.append(ans)
    return answers_dict_array
