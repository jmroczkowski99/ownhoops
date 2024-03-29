from django.db import models


class Team(models.Model):
    name_abbreviation = models.CharField(max_length=3, unique=True, blank=False, null=False)
    full_name = models.CharField(max_length=100, unique=True, blank=False, null=False)

    def __str__(self):
        return self.name_abbreviation


class Coach(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    date_of_birth = models.DateField(blank=False, null=False)
    team = models.ForeignKey('Team', related_name='coach', on_delete=models.SET_NULL, null=True, blank=True)

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
    jersey_number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.name} - DOB: {self.date_of_birth}'


class Game(models.Model):
    date = models.DateTimeField(blank=False, null=False)
    home_team = models.ForeignKey('Team', related_name='home_games', on_delete=models.CASCADE)
    away_team = models.ForeignKey('Team', related_name='away_games', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.away_team} @ {self.home_team} - {self.date}'


class Stats(models.Model):
    game = models.ForeignKey('Game', related_name='stats', on_delete=models.CASCADE)
    player = models.ForeignKey('Player', related_name='stats', on_delete=models.CASCADE)
    field_goals_made = models.IntegerField(null=False, blank=False)
    field_goals_attempted = models.IntegerField(null=False, blank=False)
    three_pointers_made = models.IntegerField(null=False, blank=False)
    three_pointers_attempted = models.IntegerField(null=False, blank=False)
    free_throws_made = models.IntegerField(null=False, blank=False)
    free_throws_attempted = models.IntegerField(null=False, blank=False)
    defensive_rebounds = models.IntegerField(null=False, blank=False)
    offensive_rebounds = models.IntegerField(null=False, blank=False)
    assists = models.IntegerField(null=False, blank=False)
    steals = models.IntegerField(null=False, blank=False)
    blocks = models.IntegerField(null=False, blank=False)
    turnovers = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return f'{self.game} - {self.player} stats'
