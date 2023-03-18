
from todo.models import TodoList, TodoItem

class TodoListService:
    def create(self, user, due_date):
        todo_list = TodoList(user=user, due_date=due_date)
        todo_list.full_clean()
        todo_list.save()
        return todo_list
    def update(self, user, todo_list_id, due_date):
        try:
            todo_list = TodoList.objects.get(user=user, id=todo_list_id)
            todo_list.due_date = due_date
            todo_list.full_clean()
            todo_list.save()
            return todo_list
        except TodoList.DoesNotExist:
            return None
        
class TodoItemService:

    def create(self, user, todo_list_id, content, is_done):
        try:
            todo_list = TodoList.objects.get(user=user, id=todo_list_id)
            todo_item = TodoItem(content=content, todo_list=todo_list, is_done=is_done)
            todo_item.full_clean()
            todo_item.save()
            return todo_item
        except TodoList.DoesNotExist:
            return None
    
    def update(self, user, todo_list_id, todo_item_id, content, is_done):
        try:
            todo_list = TodoList.objects.get(user=user, id=todo_list_id)
            todo_item = TodoItem.objects.get(todo_list=todo_list, id=todo_item_id)
            todo_item.content = content
            todo_item.is_done = is_done
            todo_item.full_clean()
            todo_item.save()
            return todo_item
        except (TodoList.DoesNotExist, TodoItem.DoesNotExist):
            return None