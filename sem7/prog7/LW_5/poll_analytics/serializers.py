from rest_framework import serializers
from polls.models import Question, Choice


class ChoiceSerializer(serializers.ModelSerializer):
    percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Choice
        fields = ['id', 'choice_text', 'votes', 'percentage']
    
    def get_percentage(self, obj):
        question = obj.question
        total_votes = sum(choice.votes for choice in question.choice_set.all())
        if total_votes == 0:
            return 0.0
        return round((obj.votes / total_votes) * 100, 2)


class QuestionSerializer(serializers.ModelSerializer):
    total_votes = serializers.SerializerMethodField()
    choices = ChoiceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'pub_date', 'total_votes', 'choices']
    
    def get_total_votes(self, obj):
        return sum(choice.votes for choice in obj.choice_set.all())

