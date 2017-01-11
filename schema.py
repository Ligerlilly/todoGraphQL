# debug tools
# import code
# code.interact(local=dict(globals(), **locals()))

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField
from models import db_session, TodoList as TodoListModel, TodoItem as TodoItemModel
from todo_list_api import TodoList
from todo_item_api import TodoItem
from mutations import Mutations

class Query(graphene.ObjectType):
    node = relay.Node.Field()

    # TodoList
    all_todo_lists = SQLAlchemyConnectionField(TodoList)
    todo_list = graphene.Field(TodoList, id=graphene.Int())

    def resolve_todo_item(self, args, into, extra_args):
        todos = TodoItemModel.query.all()
        for t in todos:
            if t.id == args.get("id"):
                return t

    # TodoItem
    all_todo_items = SQLAlchemyConnectionField(TodoItem)
    todo_item = graphene.Field(TodoItem, id=graphene.Int())

    def resolve_todo_list(self, args, info, extra_args):
        todo_lists = TodoListModel.query.all()

        for tl in todo_lists:
            if tl.id == args.get("id"):
                return tl



schema = graphene.Schema(query=Query, mutation=Mutations)

