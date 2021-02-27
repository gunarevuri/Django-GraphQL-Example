import graphene
from graphene_django import DjangoObjectType, DjangoListField,DjangoConnectionField

from movies.models import Actor, Movie
# import movies.query.Query
# import movies.query.Mutation
from movies.query import Query,Mutation

class Query(Query,graphene.ObjectType):
    pass

class Mutation(Mutation,graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)


