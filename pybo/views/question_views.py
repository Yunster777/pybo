from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question


@login_required(login_url="common:login")
def question_create(request):
    """
    질문 생성
    :param request:
    :return: get = question_form, post = question_list
    """
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect("pybo:question_list")
    else:
        form = QuestionForm()

    context = {
        "form": form,
    }

    return render(request, "pybo/question_form.html", context)


@login_required(login_url="common:login")
def question_modify(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.user != question.author:
        messages.error(request, "수정 권한이 없습니다.")
        return redirect("pybo:question_detail", pk=question.id)
    if request.method == "POST":
        form = QuestionForm(instance=question, data=request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect("pybo:question_detail", pk=question.id)
    else:
        form = QuestionForm(instance=question)

    context = {
        "form": form,
    }

    return render(request, "pybo/question_form.html", context)


@login_required(login_url="common:login")
def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.user != question.author:
        messages.error(request, "삭제 권한이 없습니다.")
        return redirect("pybo:question_detail", pk=question.id)
    question.delete()
    return redirect("pybo:question_list")


@login_required(login_url="common:login")
def question_vote(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.user == question.author:
        messages.error(request, "본인이 작성한 질문은 추천할 수 없습니다.")
    else:
        question.voter.add(request.user)

    return redirect("pybo:question_detail", pk=question.id)
