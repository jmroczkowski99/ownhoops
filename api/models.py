from django.db import models


class Team(models.Model):
    name_abbreviation = models.CharField(max_length=3, unique=True, blank=False, null=False)
    full_name = models.CharField(max_length=100, unique=True, blank=False, null=False)

    def __str__(self):
        return self.name_abbreviation


class Coach(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    date_of_birth = models.DateField(blank=True, null=True)
    current_team = models.ForeignKey('Team', related_name='coach', on_delete=models.SET_NULL, null=True, blank=True)
