

from django.test import TestCase
from django.core.exceptions import ValidationError

from todo.tests.factories import TodoItemFactory

class TodoListItemTests(TestCase):

    def test_content_cannot_be_empty(self):
        todo_item = TodoItemFactory(content="")
        with self.assertRaises(ValidationError):
            todo_item.full_clean()
    
    def test_content_cannot_be_longer_than_200_characters(self):
        todo_item = TodoItemFactory(content="a" * 201)
        with self.assertRaises(ValidationError):
            todo_item.full_clean()
    
    def test_cannot_add_item_to_locked_list(self):
        todo_item = TodoItemFactory(todo_list__locked=True)
        with self.assertRaises(ValidationError):
            todo_item.full_clean()
    
    def test_cannot_edit_item_in_locked_list(self):
        todo_item = TodoItemFactory(todo_list__locked=True)
        todo_item.content = "New content"
        with self.assertRaises(ValidationError):
            todo_item.full_clean()