"""
VISTAS
Aquí va tal cual la ejecución de la lógica de programacion creada en los serializadores
"""
from rest_framework.views import APIView  # clase general que me permite acer GET PUT y DELETE en una sola vista
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import \
    RetrieveAPIView, \
    ListAPIView, \
    CreateAPIView  # clase que se encanrga SOLO DE OBTENER adatos, por ejemplo la LISTAPIVIEW es solo de listas y así
from Personas.models import Person, Address
from Personas.api.serializers.person_serializers import *


class CreatePerson(CreateAPIView):
    serializer_class_person = PersonSerializer
    serializer_class_address = AddressSerializer

    def create(self, request, *args, **kwargs):

        serializer_person = self.serializer_class_person(data=request.data['persona'])
        if not serializer_person.is_valid():
            return Response(serializer_person.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer_address = self.serializer_class_address(data=request.data['domicilio'])
        if not serializer_address.is_valid():
            return Response(serializer_address.errors, status=status.HTTP_400_BAD_REQUEST)

        person = serializer_person.create(serializer_person.data)
        print(person.name)
        serializer_address.create((person.get_id()))

        return Response({'status': "Operación satisfactoria"}, status=status.HTTP_201_CREATED)


class GetLegalEntity(APIView):
    def get(self, request):
        table = Person.objects.filter(type_id=2)
        list = []
        for i in table:
            data = i.return_legal()
            list.append(data)
        print(list)
        return Response(list, status=status.HTTP_200_OK)


class GetNaturalPerson(APIView):
    def get(self, request):
        table = Person.objects.filter(type_id=1)
        list = []
        for i in table:
            data = i.return_natural()
            list.append(data)
        print(list)
        return Response(list, status=status.HTTP_200_OK)


class CompleteData(APIView):
    def get(self, request):
        tabla = Address.objects.all()
        list = [i.return_data() for i in tabla]  # El for pero en lista de comprensión son mucho más rápidas
        return Response(list, status=status.HTTP_200_OK)


class RetrieveAddress(RetrieveAPIView):
    serializer_class = GetAddressesPersonSerializer

    def get_queryset(self, **kwargs):
        return Person.objects.filter(**kwargs).first()

    def retrieve(self, request, *args, **kwargs):
        try:
            person_id = request.query_params['person_id']

            entity = self.get_queryset(id=person_id)
            serializer = self.serializer_class(instance=entity)
            print(serializer)
            """
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
            """
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':'operacion invalida'}, status=status.HTTP_404_NOT_FOUND)




class ListByInitial(ListAPIView):
    serializer_class = PersonSerializer

    def get_queryset(self, ini: str):
        return Person.objects.filter(name__startswith=ini)

    def list(self, request, *args, **kwargs):
        initial = request.query_params['inicial']  # AQUÍ CÓMO ESPECIFICAR O TOMAR EL CARACTER QUE ME INDIQUEN?
        print(initial)
        person = self.get_queryset(ini=initial)
        print(person)
        list = []
        for i in person:
            item = i.return_natural()
            list.append(item)
        return Response(list, status=status.HTTP_200_OK)

"""
class DecodePassword()
"""
"""
    JSON OBJECTS FOR CREATION
    
    *FOR NATURAL
    {
        "persona":{
            "name": "Chilaquiles Co",
            "last_name": "Hernandez",
            "birth_date": "1990-07-04" ,
            "email": "chilis@correo.com",
            "phone": 561324987,
            "password": "chilaquilitos",
            "description":null,
            "rfc":null,
            "type_id":1
        },
        "domicilio":{
            "street" :"Frituritas",
            "building" :"D",
            "number" :49,
            "apt" :"San Miguel",
            "zone" :"Iztapalapa",
            "cp" :56987,
            "city" :"CDMX",
            "country" :"Mexico"
        }
    }
    
    *FOR LEGAL
    {
        "persona":{
            "name": "Chilaquiles Co",
            "last_name": null,
            "birth_date": "1990-07-04" ,
            "email": "chilis@correo.com",
            "phone": 561324987,
            "password": "chilaquilitos",
            "description":"Chilaquiles desde 1879",
            "rfc":"MALF1647KFJIORE7",
            "type_id":2
        },
        "domicilio":{
            "street" :"Frituritas",
            "building" :"D",
            "number" :49,
            "apt" :"San Miguel",
            "zone" :"Iztapalapa",
            "cp" :56987,
            "city" :"CDMX",
            "country" :"Mexico"
        }
    }
"""
