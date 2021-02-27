from django.db import models
import graphene

# Create your models here.

class Actor(models.Model):
    name = models.CharField( null=False,blank=False,max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

class Movie(models.Model):
    title = models.CharField(max_length=100)
    actors = models.ManyToManyField(Actor)
    year = models.IntegerField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)



class ActorInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    age = graphene.Int()

class UpdateActorInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    age = graphene.Int(required=False)


class UpdateMovieInput(graphene.InputObjectType):
    title = graphene.String()
    id  = graphene.Int()

class MovieInput(graphene.InputObjectType):
    title = graphene.String()
    year = graphene.Int()
    actors = graphene.List(ActorInput)
    id = graphene.ID()
