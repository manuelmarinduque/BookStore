from django.urls import path
from graphene_django.views import GraphQLView

# Create your urls here.


app_name = 'libro'

urlpatterns = [
    path('', GraphQLView.as_view(graphiql=True), name='index')
]
