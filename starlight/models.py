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

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE


class Skill(models.Model):
    name = models.CharField(max_length=60)
    is_technical = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Competency(models.Model):
    class Meta:
        verbose_name_plural = 'competencies'
    INTEREST_CHOICES = (
        (1, 'Not interested'),
        (2, 'Interested to learn'),
        (3, 'Competent'),
        (4, 'Can share knowledge')
    )
    EXPERIENCE_CHOICES = (
        (1, 'Less than two years'),
        (2, 'Two to four years'),
        (3, 'Four to six years'),
        (4, 'Six to ten years'),
        (5, 'More than ten years')
    )
    skill = models.ForeignKey(Skill, null=True, on_delete=CASCADE)
    interest = models.IntegerField(choices=INTEREST_CHOICES)
    experience = models.IntegerField(choices=EXPERIENCE_CHOICES)

    def __str__(self):
        return '%s: Interest: %s, Experience: %s' % (self.skill.name, self.interest, self.experience)


class Employee(AbstractUser):

    competencies = models.ManyToManyField(Competency, blank=True, related_name='employees')

    def __repr__(self):
        return '<Employee: %s %s>' % (self.first_name, self.last_name)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
