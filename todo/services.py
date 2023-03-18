
from todo.models import TodoList, TodoItem

from todo.selectors import todo_list, todo_items, todo_item

class TodoListService:
    def create(self, user, due_date):
        todo_list = TodoList(user=user, due_date=due_date)
        todo_list.full_clean()
        todo_list.save()
        return todo_list
    
    def update(self, user, todo_list_id, due_date):
        try:
            list = todo_list(user=user, todo_list_id=todo_list_id)
            list.due_date = due_date
            list.full_clean()
            list.save()
            return list
        except TodoList.DoesNotExist:
            return None
        
class TodoItemService:

    def create(self, user, todo_list_id, content, is_done):
        try:
            list = todo_list(user=user, todo_list_id=todo_list_id)
            item = TodoItem(content=content, todo_list=list, is_done=is_done)
            item.full_clean()
            item.save()
            return item
        except TodoList.DoesNotExist:
            return None
    
    def update(self, user, todo_list_id, todo_item_id, content, is_done):
        try:
            list = todo_list(user=user, todo_list_id=todo_list_id)
            item = TodoItem.objects.get(todo_list=list, id=todo_item_id)
            item.content = content
            item.is_done = is_done
            item.full_clean()
            item.save()
            return item
        except (TodoList.DoesNotExist, TodoItem.DoesNotExist):
            return None
    
    def update_many(self, user, todo_list_id, items):
        try:
            
            list = todo_list(user=user, todo_list_id=todo_list_id)
            
            db_items = todo_items(user=user, todo_list_id=todo_list_id)
            db_items = {item.id: item for item in db_items}
            
            items_to_delete = set(db_items.keys()) - set(item['id'] for item in items)
            TodoItem.objects.filter(id__in=items_to_delete).delete()

            items_to_update = set(db_items.keys()) & set(item['id'] for item in items)
            for item_id in items_to_update:
                item = TodoItem.objects.get(todo_list=list, id=item_id)
                item.content = items[item_id]['content']
                item.is_done = items[item_id]['is_done']
                item.full_clean()
                item.save()
            
            items_to_create = set(item['id'] for item in items) - set(db_items.keys())
            for item_id in items_to_create:
                item = TodoItem(content=items[item_id]['content'], todo_list=list, is_done=items[item_id]['is_done'])
                item.full_clean()
                item.save()

            return True
        except (TodoList.DoesNotExist, TodoItem.DoesNotExist):
            return False