import base64
import csv
import io
from django.db.models import Sum
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from polls.models import Question, Choice
from .serializers import QuestionSerializer


@api_view(['GET'])
def poll_statistics(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        return Response({'error': 'Question not found'}, status=404)
    
    choices = question.choice_set.all()
    total_votes = sum(choice.votes for choice in choices)
    
    choice_stats = []
    for choice in choices:
        percentage = round((choice.votes / total_votes * 100), 2) if total_votes > 0 else 0.0
        choice_stats.append({
            'id': choice.id,
            'choice_text': choice.choice_text,
            'votes': choice.votes,
            'percentage': percentage
        })
    
    return Response({
        'question_id': question.id,
        'question_text': question.question_text,
        'pub_date': question.pub_date,
        'total_votes': total_votes,
        'choices': choice_stats
    })


@api_view(['GET'])
def overall_statistics(request):
    total_questions = Question.objects.count()
    total_choices = Choice.objects.count()
    total_votes = Choice.objects.aggregate(Sum('votes'))['votes__sum'] or 0
    
    questions_with_votes = Question.objects.annotate(
        total_votes=Sum('choice__votes')
    ).filter(total_votes__gt=0).count()
    
    return Response({
        'total_questions': total_questions,
        'total_choices': total_choices,
        'total_votes': total_votes,
        'questions_with_votes': questions_with_votes
    })


@api_view(['GET'])
def poll_chart(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        return Response({'error': 'Question not found'}, status=404)
    
    choices = question.choice_set.all()
    if not choices.exists():
        return Response({'error': 'No choices found'}, status=404)
    
    choice_texts = [choice.choice_text for choice in choices]
    votes = [choice.votes for choice in choices]
    
    format_type = request.GET.get('format', 'png').lower()
    
    if format_type == 'svg':
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(choice_texts, votes, color='steelblue', edgecolor='black')
        ax.set_xlabel('Варианты ответа', fontsize=12)
        ax.set_ylabel('Количество голосов', fontsize=12)
        ax.set_title(f'Результаты голосования: {question.question_text}', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        buffer = io.BytesIO()
        fig.savefig(buffer, format='svg', bbox_inches='tight')
        buffer.seek(0)
        svg_data = buffer.getvalue().decode('utf-8')
        plt.close(fig)
        return Response({'svg': svg_data, 'format': 'svg'})
    else:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(choice_texts, votes, color='steelblue', edgecolor='black')
        ax.set_xlabel('Варианты ответа', fontsize=12)
        ax.set_ylabel('Количество голосов', fontsize=12)
        ax.set_title(f'Результаты голосования: {question.question_text}', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        plt.close(fig)
        return Response({'image': image_base64, 'format': 'png'})


@api_view(['GET'])
def poll_chart_percentage(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        return Response({'error': 'Question not found'}, status=404)
    
    choices = question.choice_set.all()
    if not choices.exists():
        return Response({'error': 'No choices found'}, status=404)
    
    choice_texts = [choice.choice_text for choice in choices]
    votes = [choice.votes for choice in choices]
    total_votes = sum(votes)
    
    if total_votes == 0:
        return Response({'error': 'No votes yet'}, status=404)
    
    percentages = [round((v / total_votes) * 100, 1) for v in votes]
    labels = [f'{text}\n({p}%)' for text, p in zip(choice_texts, percentages)]
    
    # Создаем круговую диаграмму
    plt.figure(figsize=(10, 8))
    colors = plt.cm.Set3(range(len(choice_texts)))
    plt.pie(votes, labels=choice_texts, autopct='%1.1f%%', startangle=90, colors=colors)
    plt.title(f'Результаты голосования: {question.question_text}', fontsize=14, fontweight='bold')
    plt.axis('equal')
    
    buffer = io.BytesIO()
    format_type = request.GET.get('format', 'png').lower()
    
    if format_type == 'svg':
        plt.savefig(buffer, format='svg', bbox_inches='tight')
        buffer.seek(0)
        svg_data = buffer.getvalue().decode('utf-8')
        plt.close()
        return Response({'svg': svg_data, 'format': 'svg'})
    else:
        plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        plt.close()
        return Response({'image': image_base64, 'format': 'png'})


@api_view(['GET'])
def export_poll_json(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        return Response({'error': 'Question not found'}, status=404)
    
    choices = question.choice_set.all()
    total_votes = sum(choice.votes for choice in choices)
    
    data = {
        'question_id': question.id,
        'question_text': question.question_text,
        'pub_date': question.pub_date.isoformat(),
        'total_votes': total_votes,
        'choices': [
            {
                'id': choice.id,
                'choice_text': choice.choice_text,
                'votes': choice.votes,
                'percentage': round((choice.votes / total_votes * 100), 2) if total_votes > 0 else 0.0
            }
            for choice in choices
        ]
    }
    
    return Response(data)


@api_view(['GET'])
def export_poll_csv(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        return HttpResponse('Question not found', status=404)
    
    choices = question.choice_set.all()
    total_votes = sum(choice.votes for choice in choices)
    
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="poll_{question_id}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Question ID', question.id])
    writer.writerow(['Question Text', question.question_text])
    writer.writerow(['Publication Date', question.pub_date])
    writer.writerow(['Total Votes', total_votes])
    writer.writerow([])
    writer.writerow(['Choice Text', 'Votes', 'Percentage'])
    
    for choice in choices:
        percentage = round((choice.votes / total_votes * 100), 2) if total_votes > 0 else 0.0
        writer.writerow([choice.choice_text, choice.votes, f'{percentage}%'])
    
    return response


@api_view(['GET'])
def poll_search(request):
    queryset = Question.objects.all()
    
    # Фильтрация по дате
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        queryset = queryset.filter(pub_date__gte=date_from)
    if date_to:
        queryset = queryset.filter(pub_date__lte=date_to)
    
    # Фильтрация по тексту вопроса
    search_text = request.GET.get('search')
    if search_text:
        queryset = queryset.filter(question_text__icontains=search_text)
    
    # Сортировка
    sort_by = request.GET.get('sort_by', 'pub_date')
    sort_order = request.GET.get('order', 'desc')
    
    if sort_by == 'popularity':
        # Сортируем по общему количеству голосов
        queryset = queryset.annotate(total_votes=Sum('choice__votes'))
        if sort_order == 'asc':
            queryset = queryset.order_by('total_votes')
        else:
            queryset = queryset.order_by('-total_votes')
    elif sort_by == 'votes':
        queryset = queryset.annotate(total_votes=Sum('choice__votes'))
        if sort_order == 'asc':
            queryset = queryset.order_by('total_votes')
        else:
            queryset = queryset.order_by('-total_votes')
    elif sort_by == 'date':
        if sort_order == 'asc':
            queryset = queryset.order_by('pub_date')
        else:
            queryset = queryset.order_by('-pub_date')
    else:
        queryset = queryset.order_by('-pub_date')
    
    serializer = QuestionSerializer(queryset, many=True)
    return Response({
        'count': len(serializer.data),
        'results': serializer.data
    })
