import pytest
from django.contrib.auth.models import User
from django.test import RequestFactory
from rest_framework.test import APIClient
from api.models import Team, Coach, Player, Game, Stats


@pytest.fixture
def create_superuser():
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='password123'
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def rf():
    return RequestFactory()


@pytest.fixture
def create_first_team():
    return Team.objects.create(name_abbreviation='MIA', full_name='Miami Heat')


@pytest.fixture
def create_second_team():
    return Team.objects.create(name_abbreviation='GSW', full_name='Golden State Warriors')


@pytest.fixture
def create_third_team():
    return Team.objects.create(name_abbreviation='IND', full_name='Indiana Pacers')


@pytest.fixture
def create_first_coach(create_first_team):
    return Coach.objects.create(name='Erik Spoelstra', date_of_birth='1970-01-01', team=create_first_team)


@pytest.fixture
def create_second_coach(create_second_team):
    return Coach.objects.create(name='Steve Kerr', date_of_birth='1970-01-01', team=create_second_team)


@pytest.fixture
def create_first_player(create_first_team):
    return Player.objects.create(
        name='Jimmy Butler',
        team=create_first_team,
        date_of_birth='1988-01-01',
        country='USA',
        position='SF',
        height=201,
        weight=100,
        jersey_number=22,
    )


@pytest.fixture
def create_second_player(create_second_team):
    return Player.objects.create(
        name='Stephen Curry',
        team=create_second_team,
        date_of_birth='1988-01-01',
        country='USA',
        position='PG',
        height=188,
        weight=85,
        jersey_number=30,
    )


@pytest.fixture
def create_third_player(create_third_team):
    return Player.objects.create(
        name='Tyrese Haliburton',
        team=create_third_team,
        date_of_birth='2000-01-01',
        country='USA',
        position='PG',
        height=188,
        weight=85,
        jersey_number=0,
    )


@pytest.fixture
def create_first_game(create_first_team, create_second_team):
    return Game.objects.create(
        date="2024-01-01",
        home_team=create_first_team,
        away_team=create_second_team,
    )


@pytest.fixture
def create_second_game(create_first_team, create_third_team):
    return Game.objects.create(
        date="2024-01-01",
        home_team=create_third_team,
        away_team=create_first_team,
    )


@pytest.fixture
def create_first_statline(create_first_game, create_first_player):
    return Stats.objects.create(
        game=create_first_game,
        player=create_first_player,
        field_goals_made=3,
        field_goals_attempted=8,
        three_pointers_made=1,
        three_pointers_attempted=4,
        free_throws_made=4,
        free_throws_attempted=4,
        defensive_rebounds=8,
        offensive_rebounds=5,
        assists=1,
        steals=0,
        blocks=4,
        turnovers=1,
    )


@pytest.fixture
def create_second_statline(create_first_game, create_second_player):
    return Stats.objects.create(
        game=create_first_game,
        player=create_second_player,
        field_goals_made=5,
        field_goals_attempted=6,
        three_pointers_made=1,
        three_pointers_attempted=2,
        free_throws_made=3,
        free_throws_attempted=4,
        defensive_rebounds=1,
        offensive_rebounds=1,
        assists=3,
        steals=0,
        blocks=1,
        turnovers=5,
    )


@pytest.fixture
def create_third_statline(create_second_game, create_first_player):
    return Stats.objects.create(
        game=create_second_game,
        player=create_first_player,
        field_goals_made=5,
        field_goals_attempted=6,
        three_pointers_made=1,
        three_pointers_attempted=2,
        free_throws_made=3,
        free_throws_attempted=4,
        defensive_rebounds=1,
        offensive_rebounds=1,
        assists=3,
        steals=0,
        blocks=1,
        turnovers=5,
    )
