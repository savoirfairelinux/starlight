# Copyright (C) 2018 Savoir-faire Linux Inc. (<www.savoirfairelinux.com>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.auth.views import logout
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from starlight.forms import ObjectForm
from starlight.models import Skill, Employee, Competency


def home(request):
    skills = Skill.objects.order_by('name')
    employees = Employee.objects.all()
    return render(request, 'views/home.html', {'skills': skills, 'employees': employees, 'viewname': 'home'})


@csrf_protect
def login(request):
    return render(request, 'login/login.html')


def profile(request, id):
    employee = Employee.objects.get(pk=id)
    return render(request, 'views/profile.html', {'employee': employee, 'viewname': 'profile'})


def edit_competency(request, employee, id):
    competency = Competency.objects.get(pk=id)
    employee = Competency.objects.get(pk=employee)
    skill = competency.skill
    if request.method == 'POST':
        form = ObjectForm(request.POST, instance=competency)
        if form.is_valid():
            competency = form.save(commit=False)
            competency.skill = skill
            competency.save()
            employee.competencies.add(competency)
            employee.save()
    else:
        form = ObjectForm(instance=competency)

    return render(request, 'views/edit_competency.html', {'form': form, 'competency': competency, 'viewname': 'edit_competency'})


def logout_view(request):
    logout(request)
    return home(request)
