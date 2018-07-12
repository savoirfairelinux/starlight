# Copyright (C) 2018 Savoir-faire Linux Inc. (<www.savoirfairelinux.com>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.auth.views import logout
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from starlight.models import Skill, Employee


def home(request):
    skills = Skill.objects.order_by('name')
    employees = Employee.objects.all()
    return render(request, 'views/home.html', {'skills': skills, 'employees': employees, 'viewname': 'home'})


@csrf_protect
def login(request):
    return render(request, 'login/login.html')


def logout_view(request):
    logout(request)
    return home(request)
