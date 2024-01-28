from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import UniqueConstraint


class Team(models.Model):
    name_abbreviation = models.CharField(max_length=3, unique=True, blank=False, null=False)
    full_name = models.CharField(max_length=100, unique=True, blank=False, null=False)

    def __str__(self):
        return self.name_abbreviation


class Coach(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    date_of_birth = models.DateField(blank=True, null=True)
    current_team = models.OneToOneField('Team', related_name='coach', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Player(models.Model):
    POSITION_CHOICES = [
        ('PG', 'Point Guard'),
        ('SG', 'Shooting Guard'),
        ('SF', 'Small Forward'),
        ('PF', 'Power Forward'),
        ('C', 'Center'),
    ]

    name = models.CharField(max_length=100, blank=False, null=False)
    team = models.ForeignKey('Team', related_name='players', on_delete=models.SET_NULL, null=True, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=60, blank=False, null=False)
    position = models.CharField(max_length=2, choices=POSITION_CHOICES, blank=False, null=False)
    height = models.IntegerField(null=False, blank=False)
    weight = models.IntegerField(null=False, blank=False)
    jersey_number = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0, message="Jersey number must be at least 0."),
            MaxValueValidator(99, message="Jersey number must be at most 99."),
        ]
    )
    points_per_game = models.FloatField(null=False, blank=False)
    rebounds_per_game = models.FloatField(null=False, blank=False)
    assists_per_game = models.FloatField(null=False, blank=False)
    steals_per_game = models.FloatField(null=False, blank=False)
    blocks_per_game = models.FloatField(null=False, blank=False)
    turnovers_per_game = models.FloatField(null=False, blank=False)
    field_goal_percentage = models.FloatField(null=False, blank=False)
    three_point_field_goal_percentage = models.FloatField(null=False, blank=False)
    free_throw_percentage = models.FloatField(null=False, blank=False)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['team', 'jersey_number'],
                name='unique_team_jersey_number',
            )
        ]

    def __str__(self):
        return f"{self.name} - DOB: {self.date_of_birth}"
