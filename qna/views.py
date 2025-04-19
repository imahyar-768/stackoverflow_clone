from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Question
from .forms import QuestionForm, AnswerForm

def question_list(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'qna/question_list.html', {'questions': questions})

@login_required
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect('question_list')
    else:
        form = QuestionForm()
    return render(request, 'qna/question_form.html', {'form': form})

def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer.save()
            return redirect('question_detail', pk=pk)
    else:
        form = AnswerForm()
    return render(request, 'qna/question_detail.html', {'question': question, 'form': form})