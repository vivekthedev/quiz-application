from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    pass

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Subject(models.Model):
    name = models.CharField(max_length=200)
    sub_code = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"


class Quiz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    authored_on = models.DateTimeField(auto_now=True)
    authored_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ("-authored_on",)
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"


class Question(models.Model):
    name = models.CharField(max_length=800)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"


class Option(models.Model):
    name = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Option"
        verbose_name_plural = "Options"
