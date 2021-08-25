"""
SERIALIZADORES
Aqui solo se hace la lógica de programación tal cual
"""
from django.db.models import TextField
from rest_framework.serializers import *
from Personas.models import Person, Address


class PersonSerializer(Serializer):
    name = CharField(allow_null=False)
    last_name = CharField(allow_null=True)
    birth_date = DateField(allow_null=False)
    email = EmailField(allow_null=False)
    phone = IntegerField(max_value=9999999999, allow_null=False)
    password = CharField(allow_null=False)
    description = CharField(allow_null=True)
    rfc = CharField(allow_null=True)
    type_id = IntegerField()  # porque sino indico lo contrario sera una persona fisica

    def validate(self, attrs):
        if Person.objects.filter(email=attrs['email']).exists():
            raise ValidationError({'status': "Correo invalido"})
        if Person.objects.filter(phone=attrs['phone']).exists():
            raise ValidationError({'status': "Telefono invalido"})

        return attrs

    def create(self, validated_data):

        print(validated_data)

        if validated_data['type_id'] == 2:
            validated_data.pop('type_id')
            validated_data.pop('last_name')
            return Person.objects.create_legal(**validated_data)

        validated_data.pop('description')
        validated_data.pop('rfc')
        validated_data.pop('type_id')
        print(validated_data)
        return Person.objects.create_natural(**validated_data)

    """
    ESTOS ERAN LOS METODOS CREADOS EN UN INICIO, UNO POR CADA TIPO DE PERSONA 
    PERO SE CREE POSIBLE TENER EN UNO SOLO LA CREACION SI COMPROBAMOS QUE EXISTE UN CAMPO O NO
    PARA COMPROBAR DE QUE TIPO DE PERSONA SE TRATA
    
    def create_nat(self, validated_data):
        return Person.objects.create_natural(**self.validated_data)

    def create_leg(self, validated_data):
        return Person.objects.create_legal(**self.validated_data)
    """


class AddressSerializer(Serializer):
    street = CharField()
    building = CharField()
    number = IntegerField()
    apt = CharField()
    zone = CharField()
    cp = IntegerField()
    city = CharField()
    country = CharField()
    person = IntegerField(read_only=True)

    def validate(self, attrs):
        return attrs

    def create(self, person: int):
        print(self.validated_data)
        self.validated_data['person_id'] = person
        return Address.objects.create(**self.validated_data)


class GetAddressesPersonSerializer(Serializer):
    data = SerializerMethodField() #campo de SOLO LECTURA que ayuda a obtener instancias a través de la creacion del método que re define abajo

    def get_data(self, obj: data): #El nombre del metodo del serializador que en este caso es para un campo tipo MethodField SIEMPRE se tiene que llamar como el campo!!!
        print(obj)
        query_sets = Address.objects.select_related("person").filter(person_id=obj.id)
        list = [i.get_only_address() for i in query_sets]

        return {
            'person': obj.get_person_data(),
            'addresses': list
        }
"""
class CheckPassword(Serializer):
    user = SerializerMethodField

    def get_user(self, obj:user):

"""