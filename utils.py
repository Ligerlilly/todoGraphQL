import graphene

class Success(graphene.ObjectType):
    yeah = graphene.String()


class Error(graphene.ObjectType):
    message = graphene.String()
