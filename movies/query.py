import graphene
from movies.models import Actor,Movie, UpdateActorInput, UpdateMovieInput, ActorInput, MovieInput

from graphene_django import DjangoObjectType,DjangoListField

class ActorType(DjangoObjectType):
    class Meta:
        model = Actor

class MovieType(DjangoObjectType):
    class Meta:
        model = Movie

class Query(graphene.ObjectType):
    actor = graphene.Field(ActorType, name=graphene.String())
    actors = graphene.List(ActorType)

    movies = graphene.List(MovieType)
    movie = graphene.Field(MovieType, name = graphene.String())

    def resolve_actor(self, info,**args):
        name = args.get('name')
        if name:
            return Actor.objects.get(name = name)
        else:
            return None

    def resolve_actors(self, info, **args):
        return Actor.objects.all()
    
    def resolve_movie(self, info, **args):
        name = args.get('name')
        if name:
            return Movie.objects.get(name = name)
        else:
            return None
    
    def resolve_movies(self, info, **args):
        return Movie.objects.all()

class CreateActor(graphene.Mutation):
    class Arguments:
        input = UpdateActorInput(required = True)

    ok = graphene.Boolean()
    actor = graphene.Field(ActorType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        actor_obj = Actor(name = input.name,age = input.age)
        actor_obj.save()
        return CreateActor(ok = ok, actor = actor_obj)
        
class UpdateActor(graphene.Mutation):
    class Arguments:
        input = ActorInput(required = True)

    ok = graphene.Boolean()
    actor = graphene.Field(ActorType)

    @staticmethod
    def mutate(root, info, input = None):
        ok = False
        actor_obj = Actor.objects.get(pk = input["id"] )
        if actor_obj:
            ok = True
            actor_obj.name = input["name"]
            actor_obj.save()
            return UpdateActor(ok = ok, actor = actor_obj )

        return UpdateActor(ok = ok, actor_obj = None)

class CreateMovie(graphene.Mutation):
    class Arguments:
        input = MovieInput(required=True)

    ok = graphene.Boolean()
    movie = graphene.Field(MovieType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        actors = []
        for actor_input in input.actors:
          actor = Actor.objects.get(pk=actor_input.id)
          if actor is None:
            return CreateMovie(ok=False, movie=None)
          actors.append(actor)
        movie_instance = Movie(
          title=input.title,
          year=input.year
          )
        movie_instance.save()
        movie_instance.actors.set(actors)
        return CreateMovie(ok=ok, movie=movie_instance)


class UpdateMovie(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = MovieInput(required=True)

    ok = graphene.Boolean()
    movie = graphene.Field(MovieType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        movie_instance = Movie.objects.get(pk=id)
        if movie_instance:
            ok = True
            actors = []
            for actor_input in input.actors:
              actor = Actor.objects.get(pk=actor_input.id)
              if actor is None:
                return UpdateMovie(ok=False, movie=None)
              actors.append(actor)
            movie_instance.title=input.title
            movie_instance.year=input.year
            movie_instance.save()
            movie_instance.actors.set(actors)
            return UpdateMovie(ok=ok, movie=movie_instance)
        return UpdateMovie(ok=ok, movie=None)

class DeleteActor(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        id = graphene.ID()
    
    ok = graphene.Boolean()
    actor  = graphene.Field(ActorType)
    
    def mutate(self, info, id,  **kwargs):
        name = kwargs.get('name')
        actor_obj = Actor.objects.get(pk = id)
        actor_obj.delete()
        ok = True
        return DeleteActor(ok = ok, actor = actor_obj)
    
    
class Mutation(graphene.ObjectType):
    create_actor = CreateActor.Field()
    update_actor = UpdateActor.Field()
    create_movie = CreateMovie.Field()
    update_movie = UpdateMovie.Field()
