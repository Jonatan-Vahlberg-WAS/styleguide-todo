
from django.urls import path

from todo.views.todo_list import TodoListView, TodoListOverdueView, TodoListDoneView, TodoListCreateView

urlpatterns = [
    path('', TodoListView.as_view(), name='todo-list-list'),
    path('overdue/', TodoListOverdueView.as_view(), name='todo-list-overdue'),
    path('done/', TodoListDoneView.as_view(), name='todo-list-done'),
    path('create/', TodoListCreateView.as_view(), name='todo-list-create'),
    # path('todo-lists/<int:pk>/', TodoListDetailView.as_view(), name='todo-list-detail'),
    # path('todo-lists/<int:pk>/items/', TodoItemListCreateView.as_view(), name='todo-item-list'),
    # path('todo-lists/<int:pk>/items/<int:pk>/', TodoItemDetailView.as_view(), name='todo-item-detail'),
]