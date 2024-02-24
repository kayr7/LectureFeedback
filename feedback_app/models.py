from django.db import models
import uuid
# Create your models here.
from django.db import models


class Entity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)  # or any identifier you prefer

    def __str__(self):
        return self.name

    
class Question(models.Model):
    QUESTION_TYPES = (
        ('MC', 'Multiple Choice'),
        ('FT', 'Free Text'),
    )
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    question_type = models.CharField(max_length=2, choices=QUESTION_TYPES, default='MC')

    def __str__(self):
        return self.question_text
    

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class TextResponse(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response_text = models.TextField()

    def __str__(self):
        return f"Response to {self.question.question_text}"


