from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .forms import QuestionForm
from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "Вы не выбрали вариант ответа.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


@login_required
def create_question(request):
    """View для создания нового вопроса с вариантами ответов"""
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            # Создаем вопрос
            question = form.save(commit=False)
            question.pub_date = timezone.now()
            question.save()
            
            # Обрабатываем варианты ответов из текстовой области
            choices_text = form.cleaned_data['choices_text']
            choices_lines = [line.strip() for line in choices_text.split('\n') if line.strip()]
            
            # Создаем варианты ответов
            for choice_text in choices_lines:
                Choice.objects.create(question=question, choice_text=choice_text)
            
            messages.success(request, f'Опрос "{question.question_text}" успешно создан!')
            return redirect('polls:index')
    else:
        form = QuestionForm()
    
    return render(request, 'polls/create_question.html', {'form': form})
