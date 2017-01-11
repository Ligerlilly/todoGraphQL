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
    updateTodoList(id: 1, name: "Something Different") {
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
        result {
            id
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
'''