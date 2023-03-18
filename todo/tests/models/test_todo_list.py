

from django.test import TestCase
from django.core.exceptions import ValidationError
import datetime


from todo.tests.factories import TodoListFactory

class TodoListTests(TestCase):

    def test_due_date_cannot_be_in_the_past(self):

        todo_list = TodoListFactory( due_date=datetime.date.today() - datetime.timedelta(days=1))

        with self.assertRaises(ValidationError):
            todo_list.full_clean()
    
    def test_not_is_done_if_no_items(self):
        todo_list = TodoListFactory()
        self.assertFalse(todo_list.is_done)
    
    def test_not_is_done_if_some_items_are_not_done(self):
        todo_list = TodoListFactory()
        todo_list.items.create(content="Item 1", is_done=False)
        todo_list.items.create(content="Item 2", is_done=True)
        self.assertFalse(todo_list.is_done)
    
    def test_is_done_if_all_items_are_done(self):
        todo_list = TodoListFactory()
        todo_list.items.create(content="Item 1", is_done=True)
        todo_list.items.create(content="Item 2", is_done=True)
        self.assertTrue(todo_list.is_done)