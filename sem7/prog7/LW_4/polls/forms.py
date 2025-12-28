from django import forms
from .models import Question, Choice


class QuestionForm(forms.ModelForm):
    """Форма для создания нового вопроса"""
    choices_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 10,
            'placeholder': 'Введите варианты ответов, каждый на новой строке\nВариант 1\nВариант 2\nВариант 3'
        }),
        label='Варианты ответов',
        help_text='Введите варианты ответов, каждый на отдельной строке'
    )

    class Meta:
        model = Question
        fields = ['question_text']
        labels = {
            'question_text': 'Текст вопроса',
        }
        widgets = {
            'question_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите текст вопроса'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убираем help_text, так как он уже указан в placeholder
        if 'choices_text' in self.fields:
            self.fields['choices_text'].help_text = None

