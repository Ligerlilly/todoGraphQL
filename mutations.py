import graphene
from todo_list_api import UpdateTodoList, CreateTodoList, DeleteTodoList
from todo_item_api import UpdateTodoItem, CreateTodoItem, DeleteTodoItem

class Mutations(graphene.ObjectType):
    # TodoList mutations
    updateTodoList = UpdateTodoList.Field()
    createTodoList = CreateTodoList.Field()
    deleteTodoList = DeleteTodoList.Field()

    # TodoItem mutations
    updateTodoItem = UpdateTodoItem.Field()
    createTodoItem = CreateTodoItem.Field()
    deleteTodoItem = DeleteTodoItem.Field()