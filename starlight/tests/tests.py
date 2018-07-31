import unittest

from django.core.management import call_command
from django.test import Client

from starlight.forms import CompetencyForm, EditForm
from starlight.models import Employee, Skill, Competency


class TestFunctionality(unittest.TestCase):
    """Functional Tests"""

    def setUp(self):
        # Load fixtures
        call_command('loaddata', '/code/starlight/fixtures/fixtures.json', verbosity=0)

    """ Create a new employee and check that a new competency can be added"""
    def test_add_competency_success(self):
        client = Client()
        employee = Employee.objects.first()  # Get first employee
        skill = Skill.objects.first()  # Get first skill object

        form = CompetencyForm(data={'skill': skill, 'interest': 2, 'experience': 3}, employee=employee)
        response = client.post('/{}/profile/new_competency/'.format(employee.id), {'form': form, 'viewgroup': 'profile'})  # Call our method
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(employee.competencies.all()), 4)

    def test_edit_competency_success(self):
        client = Client()
        employee = Employee.objects.first()
        competency = employee.competencies.first()
        self.assertEqual(competency.interest, 1)
        form = EditForm(data={'interest': 2, 'experience': 3})
        self.assertTrue(form.is_valid())
        response = client.post('/{}/profile/{}/competency/'.format(employee.id, competency.id), {'form': form, 'competency': competency, 'viewgroup': 'profile'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(competency.interest, 2)
