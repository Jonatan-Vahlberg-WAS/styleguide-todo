

from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from common.utils import inline_serializer

from todo.services import TodoListService, TodoItemService
from todo.selectors import (
    todo_lists,
    todo_lists_overdue,
    todo_lists_done,
)
#abstract view


class TodoListAbstractView(APIView):
    permission_classes = [IsAuthenticated]

    list_service = TodoListService()
    item_service = TodoItemService()

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        due_date = serializers.DateField()
        is_done = serializers.BooleanField()
        is_overdue = serializers.BooleanField()
        items = inline_serializer(
            many=True,
            fields={
                "id": serializers.IntegerField(),
                "content": serializers.CharField(),
                "is_done": serializers.BooleanField(),
            },
        )


class TodoListView(TodoListAbstractView):
    pagination_class = PageNumberPagination 

    def get(self, request):
        queryset = todo_lists(request.user)
        serializer = self.OutputSerializer(queryset, many=True)
        return Response(serializer.data)

class TodoListOverdueView(TodoListAbstractView):
    pagination_class = PageNumberPagination 

    def get(self, request):
        queryset = todo_lists_overdue(request.user)
        serializer = self.OutputSerializer(queryset, many=True)
        return Response(serializer.data)
    
class TodoListDoneView(TodoListAbstractView):
    pagination_class = PageNumberPagination 

    def get(self, request):
        queryset = todo_lists_done(request.user)
        serializer = self.OutputSerializer(queryset, many=True)
        return Response(serializer.data)
    
class TodoListCreateView(TodoListAbstractView):

    class InputSerializer(serializers.Serializer):
        due_date = serializers.DateField()
        items = inline_serializer(
            many=True,
            fields={
                "content": serializers.CharField(),
                "is_done": serializers.BooleanField(),
            },
        )

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        items = serializer.validated_data.pop('items', [])
        todo_list_service = TodoListService()
        todo_item_service = TodoItemService()
        todo_list = todo_list_service.create(request.user, serializer.validated_data['due_date'])
        for item in items:
            todo_item_service.create(request.user, todo_list.id, item['content'], item['is_done'])
        output_serializer = self.OutputSerializer(todo_list)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

class TodoListDetailView(TodoListAbstractView):

    class InputSerializer(serializers.Serializer):
        due_date = serializers.DateField()
        items = inline_serializer(
            many=True,
            fields={
                "id": serializers.IntegerField(),
                "content": serializers.CharField(),
                "is_done": serializers.BooleanField(),
            },
        )

    def get(self, request, pk):
        todo_list = todo_lists(request.user).get(id=pk)
        serializer = self.OutputSerializer(todo_list)
        return Response(serializer.data)
    
    def put(self, request, pk):
        todo_list = todo_lists(request.user).get(id=pk)
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.list_service.update(todo_list, serializer.validated_data['due_date'])

        items = serializer.validated_data.pop('items', [])

        updated_items_correctly = self.item_service.update_many(request.user, todo_list, items)
        
        if not updated_items_correctly:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        output_serializer = self.OutputSerializer(todo_list)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
    
