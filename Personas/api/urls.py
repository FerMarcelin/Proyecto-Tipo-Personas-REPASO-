from django.urls import path
from Personas.api.views.person_views import *

urlpatterns = [
    path("create-person/", CreatePerson.as_view(), name='create-person'),
    path("get-legal-entity/", GetLegalEntity.as_view(), name='get-legal-entity'),
    path("get-natural-person/", GetNaturalPerson.as_view(), name='get-natural-person'),
    path("complete-data/", CompleteData.as_view(), name='complete-data'),
    path("retrieve-address/", RetrieveAddress.as_view(), name='retrieve-address'),
    path("list-by-initial/", ListByInitial.as_view(), name='list-by-initial'),

]