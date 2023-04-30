from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "quiz"
urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("create/", views.create,name="create"),
    path("create/<uuid:pk>", views.create_quiz,name="create-quiz"),
    path("question/", views.new_question, name='new-question'),
    path("detail/<uuid:pk>/", views.quiz_detail,  name="quiz_detail"),
    path("list/", views.list_quiz, name='list-quiz'),
    path("explore/",views.explore, name='explore'),
    path("start/<uuid:pk>/", views.start_quiz, name="start-quiz"),
    path("edit/<uuid:pk>/", views.edit_quiz, name="edit-quiz"),
    path("edit/<int:id>/", views.edit_question, name="edit-question"),
    path("edit/quiz/<uuid:pk>/", views.edit_quiz_form, name='edit_quiz_form'),
    path("results/", views.results, name='results'),
    path("contact/", views.Contact.as_view(), name='contact'),
    path("about/", views.About.as_view(), name='about'),
    # Authentication URLs
    path(
        "login/",
        auth_views.LoginView.as_view(redirect_authenticated_user=True),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"
    ),
    path("signup/", views.SignUp.as_view(), name="signup"),
]
