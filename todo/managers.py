

# TodoListQuerySet and TodoListManager are used to filter the TodoList

from django.db import models
from django.db.models import Q
import datetime

class TodoListQuerySet(models.QuerySet):

    def for_user(self, user):
        return self.filter(user=user)

    def overdue(self):
        return self.filter(due_date__lt=datetime.date.today())

    def done(self):
        return self.filter(items__is_done=True).distinct()

    def not_done(self):
        return self.filter(items__is_done=False).distinct()

    def locked(self):
        return self.filter(locked=True)

class TodoListManager(models.Manager):

    def get_queryset(self):
        return TodoListQuerySet(self.model, using=self._db)

    def for_user(self, user):
        return self.get_queryset().for_user(user)

    def overdue(self):
        return self.get_queryset().overdue()

    def done(self):
        return self.get_queryset().done()

    def not_done(self):
        return self.get_queryset().not_done()

    def locked(self):
        return self.get_queryset().locked()