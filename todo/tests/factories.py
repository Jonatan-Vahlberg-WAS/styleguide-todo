
import factory
from core.tests.factories import UserFactory

from todo.models import TodoList, TodoItem

class TodoListFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TodoList

    user = factory.SubFactory(UserFactory)
    due_date = factory.Faker('date_between', start_date='-1y', end_date='-1d')


class TodoItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TodoItem

    todo_list = factory.SubFactory(TodoListFactory)
    content = factory.Faker('sentence')
    is_done = factory.Faker('boolean')