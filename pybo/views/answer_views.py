from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import AnswerForm
from ..models import Question, Answer


@login_required(login_url="common:login")
def answer_create(request, pk):
    """
    답변 등록
    :param request:
    :param pk: question id
    :return: question_detail
    """
    question = get_object_or_404(Question, pk=pk)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question
            answer.create_date = timezone.now()
            answer.save()
            return redirect(
                "{}#answer_{}".format(
                    resolve_url("pybo:question_detail", pk=question.id),
                    answer.id,
                )
            )
            # return redirect("pybo:question_detail", pk=question.id)
    else:
        return HttpResponseNotAllowed("Only POST is possible.")

    context = {
        "question": question,
        "form": form,
    }
    return render(request, "pybo/question_detail.html", context)


@login_required(login_url="common:login")
def answer_modify(request, pk):
    """
    답변 수정
    :param request:
    :param pk: answer id
    :return: question_detail
    """

    answer = get_object_or_404(Answer, pk=pk)
    if request.user != answer.author:
        messages.error(request, "수정 권한이 없습니다.")
        return redirect("pybo:question_detail", pk=answer.question.id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect(
                "{}#answer_{}".format(
                    resolve_url("pybo:question_detail", pk=answer.question.id),
                    answer.id,
                )
            )
            # return redirect("pybo:question_detail", pk=answer.question.id)
    else:
        form = AnswerForm(instance=answer)

    context = {
        "form": form,
    }

    return render(request, "pybo/answer_form.html", context)


@login_required(login_url="common:login")
def answer_delete(request, pk):
    """
    답변 삭제
    :param request:
    :param pk: answer id
    :return: question_detail
    """
    answer = get_object_or_404(Answer, pk=pk)
    question_id = answer.question.id

    if request.user != answer.author:
        messages.error(request, "삭제 권한이 없습니다.")
    else:
        answer.delete()

    return redirect("pybo:question_detail", pk=question_id)


@login_required(login_url="common:login")
def answer_vote(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    if request.user == answer.author:
        messages.error(request, "본인이 작성한 답변은 추천할 수 없습니다.")
    else:
        answer.voter.add(request.user)

    return redirect(
        "{}#answer_{}".format(
            resolve_url("pybo:question_detail", pk=answer.question.id),
            answer.id,
        )
    )
    # return redirect("pybo:question_detail", pk=answer.question.id)
