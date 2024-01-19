from django.db import models


class Team(models.Model):
    name_abbreviation = CharField(max_length=3, unique=True, blank=False, null=False)
    full_name = CharField(max_length=100, unique=True, blank=False, null=False)

    def __str__(self):
        return self.name_abbreviation
    