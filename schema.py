# debug tools
# import code
# code.interact(local=dict(globals(), **locals())) 

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

    @classmethod
    def mutate(cls, instance, args, info, extra_args):
        if request.method == "POST":
            todo_item = TodoItemModel.query.get(args.get("id"))
            todo_item.destroy()
            return DeleteTodoItem(todo_item=todo_item)

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


class Mutations(graphene.ObjectType):
    updateTodoList = UpdateTodoList.Field()
    createTodoList = CreateTodoList.Field()
    deleteTodoList = DeleteTodoList.Field()
    updateTodoItem = UpdateTodoItem.Field()
    createTodoItem = CreateTodoItem.Field()
    deleteTodoItem = DeleteTodoItem.Field()

schema = graphene.Schema(query=Query, mutation=Mutations)

'''
{
    allTodoLists {
        edges {
            node {
                id
                name
                todos {
                    edges {
                        node {
                            id
                            name
                        }
                    }
                }
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

'''
{
    allTodoItems {
        edges {
            node {
                id
                name
                todoList {
                    id
                    name
                }
            }
        }
    }
}
'''

'''
{
    todoItem(id: 9) {
        id
        name
    }
}
'''

'''
mutation {
    createTodoItem(name: "new", todoListId: 1) {
        result {
            __typename
        }
    }
}
'''

'''
mutation M {
    updateTodoItem(id: 9, name: "Something Different") {
        todoItem {
            name
        }
    }
}
'''

'''
mutation {
    deleteTodoItem(id: 9) {
        todoItem {
            id
            name
        }
    }
}
'''

'''
mutation {
    deleteTodoList(id: 9) {
        todoList {
            id
            name
        }
    }
}