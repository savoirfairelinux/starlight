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
            name='Docker',
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
        data = {'skill': self.test_skill, 'interest': 1, 'experience': 1}
        url = reverse('new_competency', kwargs={'employee': self.test_user.id})
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_competency(self):
        data = {'interest': 1, 'experience': 5}
        url = reverse('edit_competency', kwargs={'employee': self.test_user.id, 'id': self.test_competency.id})
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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
        cls.client = Client()
        cls.client.login(username='employee_user', password='test1234')

    def test_add_employee(self):
        data = {'username': 'starboy', 'password': 'test12345',
                'email': 'starboy@starlight.com', 'first_name': 'star', 'last_name': 'boy', 'teams': self.test_team}
        url = reverse('new_employee')
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_employee(self):
        pass

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
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_team(self):
        data = {'name': self.test_team.name, 'description': 'description changed!'}
        url = reverse('edit_team', kwargs={'id': self.test_team.id})
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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
        pass

    def test_edit_skill(self):
        pass

    def test_remove_skill(self):
        pass
