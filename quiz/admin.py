from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Quiz, Question, Option, Subject, Result


class BaseTabularInline(admin.TabularInline):
    show_change_link = True
    extra = 3


class QuizInline(BaseTabularInline):
    model = Quiz


class QuestionInline(BaseTabularInline):
    model = Question


class OptionInline(BaseTabularInline):
    model = Option
    max_num = 3


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ["get_full_name", "username", "email"]
    search_fields = ("first_name", "last_name", "email", "username")


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ["name", "sub_code"]
    search_fields = ("name",)
    inlines = [
        QuizInline,
    ]


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ["id", "subject", "authored_by"]
    search_fields = ("subject",)
    inlines = [
        QuestionInline,
    ]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]
    search_fields = ("name",)
    inlines = [
        OptionInline,
    ]


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ["name", "is_correct"]
    search_fields = ("name",)

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'by', 'score', 'quiz']