import factory
from django.contrib.auth.models import User
from starlight.models import Competency, Employee, Skill


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)
    username = factory.Sequence(lambda x: "user{}".format(x))


class EmployeeFactory(factory.DjangoModelFactory):

    class Meta:
        model = Employee

    username = "teststar"
    first_name = "test"
    last_name = "starlight"
    password = "startest123"
    email = "test@starlight.com"


class SkillFactory(factory.DjangoModelFactory):
    class Meta:
        model = Skill

    name = factory.Faker('name')
    is_technical = True


class CompetencyFactory(factory.DjangoModelFactory):

    class Meta:
        model = Competency

    skill = factory.SubFactory(SkillFactory)
    interest = (2, 'Interested to learn')
    experience = (2, 'Two to four years')
