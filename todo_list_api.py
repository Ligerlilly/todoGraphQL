import graphene
from graphene import relay, resolve_only_args
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import db_session, TodoList as TodoListModel
from flask import request
from utils import Success, Error

class TodoList(SQLAlchemyObjectType):
    class Meta:
        model = TodoListModel
        interfaces = (relay.Node, )

class UpdateTodoList(graphene.Mutation):
    # Result field
    todo_list = graphene.Field(TodoList)

    # The input fields
    class Input:
        id = graphene.Int()
        name = graphene.String()

    @classmethod
    def mutate(cls, instance, args, info, extra_args):
        todo_lists = TodoListModel.query.all()
        if request.method == "POST":
            name = args.get("name")
            for tl in todo_lists:
                if tl.id == args.get("id"):
                    tl.name = name
                    tl.save()
                    return UpdateTodoList(todo_list=tl)

class CreateTodoListResult(graphene.Union):
    class Meta:
        types = [Success, Error]

class CreateTodoList(graphene.Mutation):
    todo_list = graphene.Field(TodoList)

    class Input:
        name = graphene.String(required=True)

    result = graphene.Field(CreateTodoListResult)

    @resolve_only_args
    def mutate(self, name):
         if request.method == "POST":
            todo_list = TodoListModel(name=name)
            todo_list.create()
            result = Success(yeah='yeah')
            return CreateTodoList(result=result)

class DeleteTodoList(graphene.Mutation):
    todo_list = graphene.Field(TodoList)

    class Input:
        id = graphene.Int(required=True)

    @classmethod
    def mutate(cls, instance, args, info, extra_args):
        if request.method == "POST":
            todo_list = TodoListModel.query.get(args.get("id"))
            todo_list.destroy()
            return DeleteTodoList(todo_list=todo_list)
