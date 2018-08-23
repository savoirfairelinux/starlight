from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
from starlight.models import Employee
from starlight.tests.factories import (
    CompetencyFactory,
    SkillFactory,
    TeamFactory
)


class TestCompetencies(TestCase):

    def setUp(cls):
        cls.test_user = Employee.objects.create_user(
            username='competency_user',
            email='testadmin@example.com',
            password='test1234'
        )
        cls.test_skill = SkillFactory(
            name='DockerTest',
            is_technical=True
        )
        cls.test_competency = CompetencyFactory(
            skill=cls.test_skill,
            interest=3,
            experience=4
        )
        cls.client = Client()
        cls.client.login(username='competency_user', password='test1234')

    def test_add_competency(self):
        data = {'skill': self.test_skill.id, 'interest': 1, 'experience': 5}
        url = reverse('new_competency', kwargs={'employee': self.test_user.id})
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # For all tests, assure redirect according to view function
        self.assertEqual(response['Location'], reverse('profile', kwargs={'id': self.test_user.id}))

    def test_edit_competency(self):
        data = {'interest': 1, 'experience': 5}
        url = reverse('edit_competency', kwargs={'employee': self.test_user.id, 'id': self.test_competency.id})
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse('profile', kwargs={'id': self.test_user.id}))

    def test_remove_competency(self):
        # Test functions with 'pass' mean that the views have not yet been created for that functionality
        pass


class TestEmployees(TestCase):

    def setUp(cls):
        cls.test_user = Employee.objects.create_superuser(
            username='employee_user',
            email='test@example.com',
            password='test1234'
        )
        cls.test_team = TeamFactory(
            name='Web',
            description='Developping web applications'
        )
        cls.test_team2 = TeamFactory(
            name='Mobile',
            description='Developping mobile applications'
        )
        cls.client = Client()
        cls.client.login(username='employee_user', password='test1234')

    def test_add_employee(self):
        data = {'username': 'starboy', 'password1': 'test12345', 'password2': 'test12345',
                'email': 'starboy@starlight.com', 'first_name': 'star', 'last_name': 'boy', 'teams': self.test_team.id}
        url = reverse('new_employee')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse('profile', kwargs={'id': 2}))  # Hardcoded ID to 2

    def test_edit_employee(self):
        data = {'username': 'starlord', 'email': 'starlord@starlight.com',
                'first_name': 'star', 'last_name': 'lord', 'teams': self.test_team2.id}
        url = reverse('edit_profile', kwargs={'id': self.test_user.id})
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse('profile', kwargs={'id': self.test_user.id}))

    def test_change_password(self):
        data = {'old_password': 'test1234', 'new_password1': 'test123456', 'new_password2': 'test123456'}
        url = reverse('change_password', kwargs={'id': self.test_user.id})
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse('profile', kwargs={'id': self.test_user.id}))

    def test_remove_employee(self):
        pass


class TestTeams(TestCase):

    def setUp(cls):
        cls.test_user = Employee.objects.create_superuser(
            username='team_user',
            email='test@example.com',
            password='test1234'
        )
        cls.test_team = TeamFactory(
            name='test_team',
            description='testing team'
        )
        cls.client = Client()
        cls.client.login(username='team_user', password='test1234')

    def test_add_team(self):
        data = {'name': 'test', 'description': 'For testing teams'}
        url = reverse('new_team')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse('teams'))

    def test_edit_team(self):
        data = {'name': self.test_team.name, 'description': 'description changed!'}
        url = reverse('edit_team', kwargs={'id': self.test_team.id})
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse('team', kwargs={'id': self.test_team.id}))

    def test_remove_team(self):
        pass


class TestSkills(TestCase):

    def setUp(cls):
        cls.test_user = Employee.objects.create_superuser(
            username='skill_user',
            email='test@example.com',
            password='test1234'
        )
        cls.client = Client()
        cls.client.login(username='skill_user', password='test1234')

    def test_add_skill(self):
        data = {'name': 'technical_skill', 'is_technical': False}
        url = reverse('new_skill')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse('all_skills'))

    def test_edit_skill(self):
        pass

    def test_remove_skill(self):
        pass
