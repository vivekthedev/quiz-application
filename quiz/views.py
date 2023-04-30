from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView
from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserForm, QuizForm, QuestionForm
from .models import User, Subject, Quiz, Question, Option, Result
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

class Home(LoginRequiredMixin, TemplateView):
    template_name = "quiz/index.html"

class Contact(TemplateView):
    template_name = "quiz/contact.html"

class About(TemplateView):
    template_name = "quiz/aboutus.html"


class SignUp(CreateView):
    model = get_user_model
    form_class = UserForm
    success_url = "/"
    template_name = "registration/signup.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]
        new_user = authenticate(self.request, username=username, password=password)
        user.save()
        if new_user is not None:
            login(self.request, user=new_user)

        return super().form_valid(form)

@login_required()
def create(request):
    subjects = Subject.objects.all().values_list('name')
    form = QuizForm()
    question_form= None
    disabled = False
    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.authored_by = request.user
            quiz.save()
            return redirect(reverse('quiz:create-quiz', kwargs={'pk':quiz.id}))
    return render(request, "quiz/create.html", {'subjects':subjects, 'disabled':disabled, 'form':form, 'question_form':question_form})

@login_required()
def create_quiz(request, pk):
    form = QuestionForm(initial={'quiz':pk})
    return render(request, 'quiz/create_questions.html', {'form':form})

def new_question(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            question = Question.objects.create(quiz_id=cd['quiz'], name=cd['question'])
            for i in [1,2,3]:
                option = Option.objects.create(name=cd[f'option_{i}'], is_correct=(i==int(cd['correct_answer'])), question=question)

            form = QuestionForm(initial={'quiz':cd['quiz']})
    
    return render(request, 'quiz/question.html', {'form':form})

@login_required()
def quiz_detail(request, pk):
    quiz = Quiz.objects.get(id=pk)
    return render(request, 'quiz/detail.html', {'quiz':quiz})

@login_required()
def list_quiz(request):
    quiz_qs = Quiz.objects.filter(authored_by=request.user)
    return render(request, 'quiz/quiz_list.html', {'quiz_qs':quiz_qs})

@login_required()
def explore(request):
    quiz_qs = Quiz.objects.exclude(authored_by=request.user).exclude(is_private=True)
    return render(request, 'quiz/quiz_list.html', {'quiz_qs':quiz_qs, 'start':True})

@login_required()
def start_quiz(request, pk):
    quiz = Quiz.objects.get(id=pk)
    count = 0
    correct = []
    given = False
    if request.method == 'POST':
        questions = quiz.question_set.all()
        for question in questions:
            option = question.option_set.all().get(is_correct=True)
            if option.id == int(request.POST.get(f'option_{question.id}')):
                count+=1
                correct.append(question)
        result = Result.objects.create(by=request.user, quiz=quiz, score=count)
        given = True
    return render(request, "quiz/start.html", {'quiz':quiz, 'score':count, 'given':given, 'correct':correct})

@login_required()
def edit_quiz(request, pk):
    quiz = Quiz.objects.get(id=pk)

    return render(request, 'quiz/edit.html', {'quiz':quiz})


@login_required()
def edit_question(request, id):
    question = Question.objects.get(id=id)
    options = question.option_set.all()
    correct = [all(i) for i in (options.values_list('is_correct'))].index(True) +1
    form = QuestionForm(initial={'quiz': question.quiz, 'question':question.name, 'option_1': options[0].name, 'option_2':options[1].name, 'option_3':options[2].name,'correct_answer':correct})
    if request.method == "POST":
        form = QuestionForm(request.POST)
        print(form.errors)
        if form.is_valid():
            cd = form.cleaned_data
            question.name = cd['question']
            question.save()
            for i,option in enumerate(options, 1):
                option.name, option.is_correct =cd[f'option_{i}'],False
                if int(cd['correct_answer']) == i: option.is_correct=True
                option.save()
            return render(request, 'quiz/return_question.html', {'question':question})
   
    return render(request, "quiz/question_form.html", {'form':form, 'id':id})

@login_required()
def edit_quiz_form(request, pk):
    quiz = Quiz.objects.get(id=pk)
    form = QuizForm(instance=quiz)
    saved = False
    if request.method == "POST":
        form = QuizForm(request.POST, instance=quiz)
        form.save()
        saved = True
    return render(request, 'quiz/quiz_info_return.html', {'form':form,'quiz':quiz, 'saved':saved})

@login_required()
def results(request):
    results_qs = Result.objects.all().filter(by=request.user).order_by('quiz')
    return render(request, 'quiz/results.html', {'results': results_qs})