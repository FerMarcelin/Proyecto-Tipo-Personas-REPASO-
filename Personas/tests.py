from django.test import TestCase
from TiposPersonas.wsgi import *
from Personas.models import Person, Address, PersonType

# Create your tests here.

"""
CREACION DE PERSONA FÍSICA

p1 = Person.objects.create_natural(name='Calu', last_name='Marcelin', birth_date=13061993, email='calu@correo.com', phone=554595876, new=True, password='chilaquilitos')
"""
# tipopersona = PersonType.objects.create(type="fisica")
# tipopersona2 = PersonType.objects.create(type="moral")
# p3 = Person.objects.create_natural(name='', last_name='Gil', birth_date="1998-09-09", email='4659@correo.com', phone=589356289, password='chilaquilitos',type_id=1 )
# print (p1)


"""
CREACION DE PERSONA MORAL

p2 = Person.objects.create_legal(name='BABEL', birth_date=24071965, email='babel@correo.com', phone=557984312, new=True, description='Implementacion de almacenamiento masivo en software', rfc='MAMP2407646F0', password='babel123')
print (p2)
"""
"""nat_person = Person.objects.get(id=12)
data = {
    'street': 'Cubo',
    'building': 'A',
    'number': 23,
    'apt': 'San Miguel',
    'zone': 'Iztapalapa',
    'cp': 13264,
    'city': 'CDMX',
    'country': 'Mexico'
}"""
# nat_person = Person.objects.get(id=12)
"""
address3 = Address.objects.create(street='Piramide', building='T',
                                  number=12,
                                  apt='Tlalpan',
                                  zone='Tlalpan',
                                  cp=36152,
                                  city='CDMX',
                                  country='Mexico',
                                  person_id=12)
"""
"""
query_params = 12
person = Person.objects.filter(id=query_params).first()
print(person.get_person_data())
dicc = dict(persona='', address='')
dicc.setdefault('persona', person.get_person_data())
print("AQUI:")
print(dicc)
"""
"""list = []
instance = Address.objects.select_related("person").filter(person_id=person.id)
for i in instance:
    item = i.get_only_address()
    list.append(item)
print(list)
list1.append(list)
print(list1)"""

"""IMPLEMENTACION PARA DESENCRIPTAR CONTRASEÑAS"""
user = Person.objects.get(email="chris@correo.com")
print(user.password)
contrasenia = "enchiladas"
raw_pass = user.check_password(contrasenia)
print (raw_pass)
if contrasenia == user.password:
    print("MATCH")
print("Noup, no son iguales")
