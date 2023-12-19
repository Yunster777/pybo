from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author_questions"
    )
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name="voter_questions")

    def __str__(self):
        return self.subject


class Answer(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author_answers"
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name="voter_answers")

    def __str__(self):
        return self.content
