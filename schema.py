import graphene
from graphene import relay, resolve_only_args
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, TodoList as TodoListModel, TodoItem as TodoItemModel
from flask import request

class Success(graphene.ObjectType):
    yeah = graphene.String()


class Error(graphene.ObjectType):
    message = graphene.String()

class TodoList(SQLAlchemyObjectType):
    class Meta:
        model = TodoListModel
        interfaces = (relay.Node, )

class TodoItem(SQLAlchemyObjectType):
    class Meta:
        model = TodoItemModel
        interfaces = (relay.Node, )

class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_todo_lists = SQLAlchemyConnectionField(TodoList)
    todo_list = graphene.Field(TodoList, id=graphene.Int())

    def resolve_todo_list(self, args, info, extra_args):
        todo_lists = TodoListModel.query.all()

        for tl in todo_lists:
            if tl.id == args.get("id"):
                return tl


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


class Mutations(graphene.ObjectType):
    updateTodoList = UpdateTodoList.Field()
    createTodoList = CreateTodoList.Field()

schema = graphene.Schema(query=Query, mutation=Mutations)

'''
{
allTodoLists {
    edges {
      node {
        id
        name
      }
    }
  }
}
'''

''' 
mutation M {
    UpdateTodoList(id: 1, name: "Something Different") {
      todoList {
        name
      }
    }
  }
'''

'''
mutation {
      createTodoList(name: "Try this out") {
        result {
          __typename
        }
      }
    }
'''

'''
{
  todoList(id: 1) {
    id
    name
  }
}
'''