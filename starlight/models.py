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
from django.contrib.auth.base_user import AbstractBaseUser


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


class Employee(AbstractBaseUser):
    def get_short_name(self):
        pass

    def get_full_name(self):
        pass

    competencies = models.ManyToManyField(Competency, blank=True, related_name='employees')

    full_name = models.CharField(
        verbose_name='Full Name',
        max_length=100
    )
    email = models.EmailField(
        verbose_name='Email Address',
        max_length=150,
        unique=True,
    )
    FULLNAME_FIELD = 'full_name'
    USERNAME_FIELD = 'email'

    def __repr__(self):
        return '<User: %s>' % self.full_name

    def __str__(self):
        return self.full_name
