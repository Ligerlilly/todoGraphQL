# debug tools
# import code
# code.interact(local=dict(globals(), **locals()))

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField
from models import db_session, TodoList as TodoListModel, TodoItem as TodoItemModel
from todo_list_api import TodoList, UpdateTodoList, CreateTodoList, DeleteTodoList
from todo_item_api import TodoItem, UpdateTodoItem, CreateTodoItem, DeleteTodoItem

class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_todo_lists = SQLAlchemyConnectionField(TodoList)
    todo_list = graphene.Field(TodoList, id=graphene.Int())
    all_todo_items = SQLAlchemyConnectionField(TodoItem)
    todo_item = graphene.Field(TodoItem, id=graphene.Int())

    def resolve_todo_item(self, args, into, extra_args):
        todos = TodoItemModel.query.all()
        for t in todos:
            if t.id == args.get("id"):
                return t

    def resolve_todo_list(self, args, info, extra_args):
        todo_lists = TodoListModel.query.all()

        for tl in todo_lists:
            if tl.id == args.get("id"):
                return tl

class Mutations(graphene.ObjectType):
    updateTodoList = UpdateTodoList.Field()
    createTodoList = CreateTodoList.Field()
    deleteTodoList = DeleteTodoList.Field()
    updateTodoItem = UpdateTodoItem.Field()
    createTodoItem = CreateTodoItem.Field()
    deleteTodoItem = DeleteTodoItem.Field()

schema = graphene.Schema(query=Query, mutation=Mutations)

