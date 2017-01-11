import graphene
from graphene import relay, resolve_only_args
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import db_session, TodoList as TodoListModel, TodoItem as TodoItemModel
from flask import request
from utils import Success, Error
from todo_list_api import TodoList


class TodoItem(SQLAlchemyObjectType):
    class Meta:
        model = TodoItemModel
        interfaces = (relay.Node, )

class UpdateTodoItem(graphene.Mutation):
    # Result field
    todo_item = graphene.Field(TodoItem)

    # The input fields
    class Input:
        id = graphene.Int()
        name = graphene.String()

    @classmethod
    def mutate(cls, instance, args, info, extra_args):
        todo_items = TodoItemModel.query.all()
        if request.method == "POST":
            name = args.get("name")
            for t in todo_items:
                if t.id == args.get("id"):
                    t.name = name
                    t.save()
                    return UpdateTodoItem(todo_item=t)

class CreateTodoItemResult(graphene.Union):
    class Meta:
        types = [Success, Error]

class CreateTodoItem(graphene.Mutation):
    todo_item = graphene.Field(TodoItem)

    class Input:
        name = graphene.String(required=True)
        todo_list_id = graphene.Int(required=True)

    result = graphene.Field(CreateTodoItemResult)

    @resolve_only_args
    def mutate(self, name, todo_list_id):
        if request.method == "POST":
            todo_list = TodoListModel.query.get(todo_list_id)
            todo_item = TodoItemModel(name=name, todo_list=todo_list)
            todo_item.create()
            result = Success(yeah='yeah')
            return CreateTodoItem(result=result)

class DeleteTodoItem(graphene.Mutation):
    todo_item = graphene.Field(TodoItem)

    class Input:
        id = graphene.Int(required=True)

    result = graphene.Field(TodoList)

    @classmethod
    def mutate(cls, instance, args, info, extra_args):
        if request.method == "POST":
            todo_item = TodoItemModel.query.get(args.get("id"))
            todo_list_id = todo_item.todo_list_id
            todo_item.destroy()
            result = TodoListModel.query.get(todo_list_id)
            return DeleteTodoItem(result=result)