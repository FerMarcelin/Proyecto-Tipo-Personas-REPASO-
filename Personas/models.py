from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser


# Create your models here.
class PersonType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=80)


class ManagerUser(BaseUserManager):  # PREGUNTA!! ¿para qué funciona exqactamente esta clase?
    def create_natural(self, name, last_name, birth_date, email, phone, password=None):
        if name is None:
            raise TypeError("No hay nombre")
        if last_name is None:
            raise TypeError("No hay apellido")
        if email is None:
            raise TypeError("No hay email")

        natural_person = self.model(name=name, last_name=last_name, birth_date=birth_date, email=email, phone=phone,
                                    username=email)  # puedo quitar new ya que será por default

        natural_person.set_password(password)
        natural_person.save(using=self._db)
        return natural_person

    def create_legal(self, name, birth_date, email, phone, description, rfc, password=None):
        if name is None:
            raise TypeError("No hay nombre")
        if email is None:
            raise TypeError("No hay email")

        legal_entity = self.model(name=name, birth_date=birth_date, email=email, phone=phone, username=email,
                                  description=description, rfc=rfc)

        legal_entity.type_id = 2
        legal_entity.set_password(password)
        legal_entity.save(using=self._db)
        return legal_entity


class Person(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=True,
                                 blank=True)  # Se recomienda en char y text no ocupar null=true a menos que sea unique para evitar reduncdancia ya que si no, tendría dos posibles valores para "no data" NULL y cadena vacia
    birth_date = models.DateField(null=False, blank=False)
    email = models.EmailField(max_length=255, null=False, blank=False, unique=True)
    phone = models.IntegerField(null=False, blank=False, unique=True)
    username = models.CharField(max_length=255, null=False, blank=False)
    password = models.CharField(max_length=200, null=False, blank=False)
    new = models.BooleanField(default=True)  # NOTA: ocupar valor por defauilt
    description = models.CharField(max_length=255, blank=True)
    rfc = models.CharField(max_length=255, null=True, blank=True)
    type = models.ForeignKey(PersonType, on_delete=models.DO_NOTHING, default=1)

    objects = ManagerUser()
    """
    USERNAME_FIELD especifica que dato se estará usando para ingresar al sitio
    en este caso será por correo
    """
    USERNAME_FIELD = 'email'

    class Meta:
        db_table = "People"
        ordering = ['id']
        verbose_name = "person"

    def get_id(self):
        return self.id

    def return_natural(self):
        return {'name': self.name, 'last_name': self.last_name, 'username': self.username, 'phone': self.phone}

    def return_legal(self):
        return {'name': self.name, 'rfc': self.rfc}

    def get_person_data(self):
        return {
            'id': self.id,
            'name': self.name,
            'last_name': self.last_name,
            'birth_date': self.birth_date,
            'email': self.email,
            'phone': self.phone,
            'username': self.username,
            'password': self.password,
            'new': self.new,
            'description': self.description,
            'rfc': self.rfc
        }


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    street = models.CharField(max_length=100, null=False, blank=False)
    building = models.CharField(max_length=20, null=True, blank=True)
    number = models.IntegerField(null=False, blank=False)
    apt = models.CharField(max_length=100, null=False, blank=False)
    zone = models.CharField(max_length=100, null=False, blank=False)
    cp = models.IntegerField(null=False, blank=False)
    city = models.CharField(max_length=100, null=False, blank=False)
    country = models.CharField(max_length=100, null=False, blank=False)
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING, null=False, blank=False)

    """
    Class Meta: sirve para configurar los metadatos para la DB es decir
    como quiero que se ordene y el nombre de la tabbla en la DB
    """

    class Meta:
        db_table = "Addresses"
        ordering = ['id']
        verbose_name = "address"

    def get_full_address_and_person(self):
        return {
            'street': self.street,
            'building': self.building,
            'number': self.number,
            'apt': self.apt,
            'zone': self.zone,
            'cp': self.cp,
            'city': self.city,
            'country': self.country,
            'person': self.person.get_person_data()
        }

    def get_only_address(self):
        return {
            'street': self.street,
            'building': self.building,
            'number': self.number,
            'apt': self.apt,
            'zone': self.zone,
            'cp': self.cp,
            'city': self.city,
            'country': self.country
        }
