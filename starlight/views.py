# Copyright (C) 2018 Savoir-faire Linux Inc. (<www.savoirfairelinux.com>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from starlight.forms import EditForm, CompetencyForm, EmployeeForm, TeamForm, FilterTeamForm, AddtoTeamForm
from starlight.models import Skill, Employee, Competency, Team


def home(request):
    if request.method == 'POST':
        form = FilterTeamForm(request.POST)
        if form.is_valid():
            filter_name = Team.objects.get(pk=form.cleaned_data['name']).name \
                if not form.cleaned_data['name'] == '0' else 'unassigned'
        else:
            filter_name = None
    else:
        form = FilterTeamForm()
        filter_name = None

    if filter_name:
        if filter_name == 'unassigned':
            teams = None
            employees = Employee.objects.filter(teams__isnull=True)
        else:
            teams = Team.objects.get(name=filter_name)
            employees = Employee.objects.filter(teams=teams)
    else:
        teams = Team.objects.all()
        employees = Employee.objects.all()
        
    skills = Skill.objects.order_by('name')

    return render(request, 'views/home.html', {'form': form, 'skills': skills, 'employees': employees, 'teams': teams, 'viewgroup': 'home'})


@csrf_protect
def login(request):
    return render(request, 'login/login.html')


def profile(request, id):
    employee = Employee.objects.get(pk=id)
    return render(request, 'profile_views/profile.html', {'employee': employee, 'viewgroup': 'profile'})


def edit_competency(request, employee, id):
    competency = Competency.objects.get(pk=id)
    employee = Employee.objects.get(pk=employee)
    if not request.user.has_perm('starlight.can_change_user') and not employee == request.user:
        raise PermissionDenied({"message: You do not have permission to edit this"})
    skill = competency.skill
    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            interest = form.cleaned_data['interest']
            experience = form.cleaned_data['experience']
            competency_new, created = employee.competencies.all().get_or_create(skill=skill, interest=interest, experience=experience)
            if created:
                employee.competencies.add(competency_new)
                employee.competencies.remove(competency)
                messages.success(request, 'Competency succesfully edited')

            return HttpResponseRedirect('/{}/profile/'.format(employee.id))

    else:
        form = EditForm()

    return render(request, 'profile_views/edit_competency.html', {'form': form, 'competency': competency, 'viewgroup': 'profile'})


def new_competency(request, employee):
    employee = Employee.objects.get(pk=employee)
    if not request.user.has_perm('starlight.can_change_user') and not employee == request.user:
        raise PermissionDenied({"message: You do not have permission to edit this"})
    if request.method == 'POST':
        form = CompetencyForm(request.POST, employee=employee)
        if form.is_valid():
            skill = form.cleaned_data['skill']
            competency_new = form.save(commit=False)

            if employee.competencies.all().filter(skill=skill).exists():
                employee.competencies.remove(employee.competencies.all().get(skill=skill))
                competency_new.save()
                employee.competencies.add(competency_new)
                messages.success(request, 'Competency with this skill already exists, it has been updated')
            else:
                competency_new.save()
                employee.competencies.add(competency_new)
                messages.success(request, 'Competency successfully added')

            return HttpResponseRedirect('/{}/profile/'.format(employee.id))

    else:
        form = CompetencyForm(employee=employee)

    return render(request, 'profile_views/new_competency.html', {'form': form, 'viewgroup': 'profile'})


def logout_view(request):
    logout(request)
    return home(request)


def all_profiles(request):
    employees = Employee.objects.all()
    return render(request, 'views/all_profiles.html', {'employees': employees, 'viewgroup': 'all_profiles'})


@user_passes_test(lambda u: u.has_perm('starlight.can_change_user'))
def new_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            teams = form.cleaned_data['teams']
            employee = Employee.objects.create(username=username, email=email, first_name=first_name, last_name=last_name)
            employee.teams.add(*teams)
            employee.set_password(password)
            employee.save()
            return HttpResponseRedirect('/{}/profile/'.format(employee.id))
    else:
        form = EmployeeForm()

    return render(request, 'views/new_employee.html', {'form': form})


def view_all_teams(request):
    teams = Team.objects.all()
    return render(request, 'views/teams.html', {'teams': teams, 'viewgroup': 'teams'})


def view_team(request, id):
    team = Team.objects.get(pk=id)
    employees = Employee.objects.filter(teams=team)
    if request.method == 'POST':
        form = AddtoTeamForm(request.POST)
        if form.is_valid():
            employee = form.cleaned_data['employee']
            employee.teams.add(team)
    else:
        form = AddtoTeamForm()

    return render(request, 'views/team.html', {'form': form, 'team': team, 'employees': employees, 'viewgroup': 'teams'})


@user_passes_test(lambda u: u.has_perm('starlight.can_change_team'))
def new_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save()
            return redirect('teams')
    else:
        form = TeamForm()

    return render(request, 'views/edit_team.html', {'form': form, 'viewgroup': 'teams', 'form_type': 'new'})


@user_passes_test(lambda u: u.has_perm('starlight.can_change_team') and u.has_perm('starlight.can_change_user'))
def remove_from_team(request, team, id):
    team = Team.objects.get(pk=team)
    employee = Employee.objects.get(pk=id)
    if team in employee.teams.all():
        employee.teams.remove(team)

    return redirect('team', id=team.id)


@user_passes_test(lambda u: u.has_perm('starlight.can_change_team'))
def edit_team(request, id):
    team = Team.objects.get(pk=id)
    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect('team', id=team.id)
    else:
        form = TeamForm()

    return render(request, 'views/edit_team.html', {'team': team, 'form': form, 'viewgroup': 'teams', 'form_type': 'edit'})
