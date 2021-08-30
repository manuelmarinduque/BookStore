from django.urls import path
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt


# Create your urls here.

urlpatterns = [
    path('', csrf_exempt(GraphQLView.as_view(graphiql=True)))
]
