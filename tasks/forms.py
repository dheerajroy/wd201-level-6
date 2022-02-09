from django.forms import ModelForm
from .models import Task

class CreateUpdateTaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
        
    class Meta:
        model = Task
        fields = ('title', 'description', 'completed', 'priority')
