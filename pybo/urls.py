from django.urls import path
from .views import base_views, question_views, answer_views

app_name = "pybo"
urlpatterns = [
    # base_views.py
    path("", base_views.question_list, name="question_list"),
    path("<int:pk>/", base_views.question_detail, name="question_detail"),
    # question_views.py
    path("question/create/", question_views.question_create, name="question_create"),
    path(
        "question/modify/<int:pk>/",
        question_views.question_modify,
        name="question_modify",
    ),
    path(
        "question/delete/<int:pk>/",
        question_views.question_delete,
        name="question_delete",
    ),
    path("question/vote/<int:pk>/", question_views.question_vote, name="question_vote"),
    # answer_views.py
    path("answer/create/<int:pk>/", answer_views.answer_create, name="answer_create"),
    path("answer/modify/<int:pk>/", answer_views.answer_modify, name="answer_modify"),
    path("answer/delete/<int:pk>/", answer_views.answer_delete, name="answer_delete"),
    path("answer/vote/<int:pk>/", answer_views.answer_vote, name="answer_vote"),
]
