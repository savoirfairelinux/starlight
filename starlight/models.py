# Copyright (C) 2017 Savoir-faire Linux Inc. (<www.savoirfairelinux.com>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

from django.db import models
from django.db.models.deletion import SET


class Experience(models.Model):
    experience_level = models.CharField(max_length=60)


class Interest(models.Model):
    interest_level = models.CharField(max_length=60)


class Competency(models.Model):
    name = models.CharField(max_length=60)
    interest = models.ForeignKey(Interest, on_delete=SET('Not interested'))
    experience = models.ForeignKey(Experience, on_delete=SET('Less than two years'))

    def __repr__(self):
        return '<Competency: %s>' % self.name

    def __str__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=60)
    password = models.CharField(max_length=60)
    email = models.CharField(max_length=75)
    competencies = models.ManyToManyField(Competency, blank=True, related_name='employees')

    def __repr__(self):
        return '<User: %s>' % self.name

    def __str__(self):
        return self.name