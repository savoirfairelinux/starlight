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
from django.db.models.deletion import CASCADE


class Skill(models.Model):
    name = models.CharField(max_length=60)
    is_technical = models.BooleanField(default=True)


class Competency(models.Model):
    INTEREST_CHOICES = (
        ('1', 'Not interested'),
        ('2', 'Interested to learn'),
        ('3', 'Competent'),
        ('4', 'Can share knowledge')
    )
    EXPERIENCE_CHOICES = (
        ('0-2', 'Less than two years'),
        ('2-4', 'Two to four years'),
        ('4-6', 'Four to six years'),
        ('6-10', 'Six to ten years'),
        ('10+', 'More than ten years')
    )
    skill = models.ForeignKey(Skill, null=True, on_delete=CASCADE)
    interest = models.CharField(max_length=50, choices=INTEREST_CHOICES)
    experience = models.CharField(max_length=50, choices=EXPERIENCE_CHOICES)


class Employee(models.Model):
    name = models.CharField(max_length=60)
    password = models.CharField(max_length=60)
    email = models.CharField(max_length=75)
    competencies = models.ManyToManyField(Competency, blank=True, related_name='employees')

    def __repr__(self):
        return '<User: %s>' % self.name

    def __str__(self):
        return self.name