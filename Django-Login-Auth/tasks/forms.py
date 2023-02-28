from django.forms import ModelForm
from .models import Task

class TasksForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        