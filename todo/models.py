from common.models import BaseModel
from django.db import models
from django.core.exceptions import ValidationError
import datetime

# Create your models here.

class TodoList(BaseModel):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    due_date = models.DateField(null=True, blank=True)
    locked = models.BooleanField(default=False)

    @property
    def is_overdue(self):
        return self.due_date < datetime.date.today()
    
    @property
    def is_done(self):
        if len(self.items.all()) == 0:
            return False
        return len(self.items.filter(is_done=False)) == 0

    def clean(self):
        if self.due_date < datetime.date.today():
            raise ValidationError("Due date cannot be in the past")

    def __str__(self):
        return f"Todo list for {self.user.username} {self.pk}"

class TodoItem(BaseModel):
    content = models.CharField(max_length=200)
    is_done = models.BooleanField(default=False)
    todo_list = models.ForeignKey(TodoList, on_delete=models.CASCADE, related_name='items')

    def clean(self):
        if self.content == "":
            raise ValidationError("Content cannot be empty")
        elif len(self.content) > 200:
            raise ValidationError("Content cannot be longer than 200 characters")
        
        if self.todo_list.locked:
            raise ValidationError("Todo list is locked")

    def __str__(self):
        return f"Todo item {self.pk} for {self.todo_list.pk}"