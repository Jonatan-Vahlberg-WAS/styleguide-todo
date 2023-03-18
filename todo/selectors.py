
from .models import TodoList

### TodoLists

def todo_lists(*, user):
    return TodoList.objects.for_user(user=user)

def todo_lists_overdue(*, user):
    return todo_lists(user).overdue()

def todo_lists_done(*, user):
    return todo_lists(user).done()

def todo_lists_not_done(*, user):
    return todo_lists(user).not_done()

def todo_list(*, user, todo_list_id):
    return todo_lists(user).get(id=todo_list_id)

### TodoItems

def todo_items(*, user, todo_list_id):
    return todo_list(user=user, todo_list_id=todo_list_id).items.all()

def todo_item(*, user, todo_list_id, todo_item_id):
    return todo_items(user=user, todo_list_id=todo_list_id).get(id=todo_item_id)