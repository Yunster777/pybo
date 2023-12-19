from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from ..models import Question


def question_list(request):
    """
    question list 페이지
    :param request:
    :return: question_list
    """
    page = request.GET.get("page", "1")  # get 파라미터 page 받아오기
    kw = request.GET.get("kw", "")
    q_list = Question.objects.order_by("-create_date")

    if kw:
        q_list = q_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()

    paginator = Paginator(q_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {
        "question_list": page_obj,
        "page": page,
        "kw": kw,
    }
    return render(request, "pybo/question_list.html", context)


def question_detail(request, pk):
    """
    question 상세 페이지
    :param request:
    :param pk: question id
    :return: question_detail
    """
    question = get_object_or_404(Question, pk=pk)
    context = {
        "question": question,
    }
    return render(request, "pybo/question_detail.html", context)
