# Copyright (C) 2018 Savoir-faire Linux Inc. (<www.savoirfairelinux.com>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
from django.shortcuts import render_to_response
from django.template import RequestContext

from starlight.models import Skill, Employee


def home(request):
    skills = Skill.objects.order_by('name')
    employees = Employee.objects.all()
    return render_to_response('views/home.html', {'skills': skills, 'employees': employees, 'viewname': 'home'})


def login(request):
    return render_to_response('login/login.html', {'viewname': 'login'})
