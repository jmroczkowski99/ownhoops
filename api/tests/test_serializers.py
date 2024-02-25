import pytest
from django.urls import reverse
from api.serializers import CoachSerializer, PlayerSerializer, TeamSerializer, GameSerializer, StatsSerializer
from api.models import Coach, Player, Game, Stats
from datetime import date, timedelta


class TestTeamSerializer:
    @pytest.mark.django_db
    def test_valid_empty_team(self, rf):
        request = rf.get('/dummy-url/')

        data = {
            'name_abbreviation': 'TES',
            'full_name': 'Test Team',
        }

        serializer = TeamSerializer(data=data, context={'request': request})
        assert serializer.is_valid()
        assert serializer.save()
        assert serializer.data['name_abbreviation'] == data['name_abbreviation']
        assert serializer.data['full_name'] == data['full_name']
        assert serializer.data['coach'] == {'id': None, 'name': '', 'url': None}
        assert serializer.data['players'] == []
        assert serializer.data['games'] == []

    @pytest.mark.django_db
    def test_valid_empty_team_numbers_in_name(self, rf):
        request = rf.get('/dummy-url/')

        data = {
            'name_abbreviation': 'TES',
            'full_name': 'Test T3am',
        }

        serializer = TeamSerializer(data=data, context={'request': request})
        assert serializer.is_valid()
        assert serializer.save()
        assert serializer.data['name_abbreviation'] == data['name_abbreviation']
        assert serializer.data['full_name'] == data['full_name']
        assert serializer.data['coach'] == {'id': None, 'name': '', 'url': None}
        assert serializer.data['players'] == []
        assert serializer.data['games'] == []

    @pytest.mark.django_db
    def test_valid_empty_team_name_starting_with_numbers(self, rf):
        request = rf.get('/dummy-url/')

        data = {
            'name_abbreviation': 'PHI',
            'full_name': 'Philadelphia 76ers',
        }

        serializer = TeamSerializer(data=data, context={'request': request})
        assert serializer.is_valid()
        assert serializer.save()
        assert serializer.data['name_abbreviation'] == data['name_abbreviation']
        assert serializer.data['full_name'] == data['full_name']
        assert serializer.data['coach'] == {'id': None, 'name': '', 'url': None}
        assert serializer.data['players'] == []
        assert serializer.data['games'] == []

    @pytest.mark.django_db
    def test_valid_team(self, create_first_team, create_second_team, rf):
        request = rf.get('/dummy-url/')

        team_data = {
            'name_abbreviation': 'TES',
            'full_name': 'Test Team',
        }

        serializer = TeamSerializer(data=team_data, context={'request': request})
        assert serializer.is_valid(), serializer.errors
        team = serializer.save()

        coach_data = {
            'name': 'Valid Coach',
            'date_of_birth': '1980-01-01',
            'team': team,
        }

        player_one_data = {
            'name': 'Valid Player',
            'date_of_birth': '1980-01-01',
            'team': team,
            'country': 'USA',
            'position': 'SF',
            'height': 201,
            'weight': 100,
            'jersey_number': 22,
        }

        player_two_data = {
            'name': 'Valid Pllayer',
            'date_of_birth': '1981-01-01',
            'team': team,
            'country': 'Poland',
            'position': 'PG',
            'height': 202,
            'weight': 103,
            'jersey_number': 11,
        }

        game_one_data = {
            'date': '2024-01-02 20:00:00',
            'home_team': team,
            'away_team': create_first_team,
        }

        game_two_data = {
            'date': '2024-02-01 20:00:00',
            'home_team': create_second_team,
            'away_team': team,
        }

        Coach.objects.create(**coach_data)
        Player.objects.create(**player_one_data)
        Player.objects.create(**player_two_data)
        Game.objects.create(**game_one_data)
        Game.objects.create(**game_two_data)

        team.refresh_from_db()

        assert serializer.data['name_abbreviation'] == team_data['name_abbreviation']
        assert serializer.data['full_name'] == team_data['full_name']
        assert serializer.data['coach'] == {'id': 1, 'name': coach_data['name'], 'url': 'http://testserver/coaches/1/'}
        assert serializer.data['players'] == [
            {
                'id': 1,
                'name': player_one_data['name'],
                'position': player_one_data['position'],
                'jersey_number': player_one_data['jersey_number'],
                'url': 'http://testserver/players/1/'
            },
            {
                'id': 2,
                'name': player_two_data['name'],
                'position': player_two_data['position'],
                'jersey_number': player_two_data['jersey_number'],
                'url': 'http://testserver/players/2/'
            }
        ]
        assert serializer.data['games'] == [
            {
                'url': 'http://testserver/games/1/',
                'id': 1,
                'info': f'{game_one_data["away_team"]} @ {game_one_data["home_team"]} - 2024-01-02T20:00:00Z',
                'box_score': 'http://testserver/games/1/stats/',
            },
            {
                'url': 'http://testserver/games/2/',
                'id': 2,
                'info': f'{game_two_data["away_team"]} @ {game_two_data["home_team"]} - 2024-02-01T20:00:00Z',
                'box_score': 'http://testserver/games/2/stats/',
            }
        ]

    @pytest.mark.django_db
    def test_team_invalid_name_abbreviation_too_short(self):
        data = {
            'name_abbreviation': 'TE',
            'full_name': 'Test Team',
        }

        serializer = TeamSerializer(data=data)
        assert not serializer.is_valid()
        assert 'Team name abbreviation must contain 3 letters.' in serializer.errors['name_abbreviation']

    @pytest.mark.django_db
    def test_team_invalid_name_abbreviation_too_long(self):
        data = {
            'name_abbreviation': 'TEST',
            'full_name': 'Test Team',
        }

        serializer = TeamSerializer(data=data)
        assert not serializer.is_valid()
        assert 'Ensure this field has no more than 3 characters.' in serializer.errors['name_abbreviation']

    @pytest.mark.django_db
    def test_team_invalid_name_abbreviation_numbers(self):
        data = {
            'name_abbreviation': 'T35',
            'full_name': 'Test Team',
        }

        serializer = TeamSerializer(data=data)
        assert not serializer.is_valid()
        assert 'Team name abbreviation can contain only letters.' in serializer.errors['name_abbreviation']

    @pytest.mark.django_db
    def test_team_invalid_name_abbreviation_special_chars(self):
        data = {
            'name_abbreviation': 'T/E',
            'full_name': 'Test Team',
        }

        serializer = TeamSerializer(data=data)
        assert not serializer.is_valid()
        assert 'Team name abbreviation can contain only letters.' in serializer.errors['name_abbreviation']

    @pytest.mark.django_db
    def test_team_invalid_name_abbreviation_not_uppercase(self):
        data = {
            'name_abbreviation': 'Tes',
            'full_name': 'Test Team',
        }

        serializer = TeamSerializer(data=data)
        assert not serializer.is_valid()
        assert 'Team name abbreviation should be uppercase.' in serializer.errors['name_abbreviation']

    @pytest.mark.django_db
    def test_team_invalid_full_name_special_chars(self):
        data = {
            'name_abbreviation': 'TES',
            'full_name': 'Test Te@m',
        }

        serializer = TeamSerializer(data=data)
        assert not serializer.is_valid()
        assert 'Team name can contain only letters and numbers.' in serializer.errors['full_name']

    @pytest.mark.django_db
    def test_team_invalid_full_name_not_capitalized(self):
        data = {
            'name_abbreviation': 'TES',
            'full_name': 'test Team',
        }

        serializer = TeamSerializer(data=data)
        assert not serializer.is_valid()
        assert 'Team name should be capitalized.' in serializer.errors['full_name']

    @pytest.mark.django_db
    def test_team_invalid_full_name_all_caps(self):
        data = {
            'name_abbreviation': 'TES',
            'full_name': 'TEST TEAM',
        }

        serializer = TeamSerializer(data=data)
        assert not serializer.is_valid()
        assert 'Team name should be capitalized.' in serializer.errors['full_name']


class TestCoachSerializer:
    @pytest.mark.django_db
    def test_valid_coach(self, create_first_team, rf):
        request = rf.get('/dummy-url/')

        data = {
            'name': 'Valid Coach',
            'date_of_birth': '1980-01-01',
            'team': reverse('team-detail', args=[create_first_team.id]),
        }

        serializer = CoachSerializer(data=data, context={'request': request})
        assert serializer.is_valid()
        assert serializer.save()
        assert serializer.data['name'] == data['name']
        assert serializer.data['date_of_birth'] == data['date_of_birth']
        assert reverse('team-detail', args=[create_first_team.id]) in serializer.data['team']
        assert serializer.data['team_name_abbreviation'] == create_first_team.name_abbreviation

    @pytest.mark.django_db
    def test_valid_coach_no_team(self, rf):
        request = rf.get('/dummy-url/')

        data = {
            'name': 'Valid Coach',
            'date_of_birth': '1980-01-01',
        }

        serializer = CoachSerializer(data=data, context={'request': request})
        assert serializer.is_valid()
        assert serializer.save()
        assert serializer.data['name'] == data['name']
        assert serializer.data['date_of_birth'] == data['date_of_birth']
        assert serializer.data['team'] is None
        assert serializer.data.get('team_name_abbreviation') is None

    @pytest.mark.django_db
    def test_coach_nonexisting_team(self):
        data = {
            'name': 'Valid Coach',
            'date_of_birth': '1980-01-01',
            'team': 'ABC',
        }

        serializer = CoachSerializer(data=data)
        assert not serializer.is_valid()
        assert serializer.errors['team']

    @pytest.mark.django_db
    def test_coach_already_coached_team(self, create_first_coach, create_first_team):
        data = {
            'name': 'Valid Coach',
            'date_of_birth': '1980-01-01',
            'team': reverse('team-detail', args=[create_first_team.id]),
        }

        serializer = CoachSerializer(data=data)
        assert not serializer.is_valid()
        assert 'This team already has a coach.' in serializer.errors['non_field_errors']

    @pytest.mark.django_db
    def test_coach_invalid_name_nonletters(self, create_first_team):
        data = {
            'name': 'Va3lid Coach',
            'date_of_birth': '1980-01-01',
            'team': reverse('team-detail', args=[create_first_team.id]),
        }

        serializer = CoachSerializer(data=data)
        assert not serializer.is_valid()
        assert 'Name should only contain letters.' in serializer.errors['name']

    @pytest.mark.django_db
    def test_coach_invalid_name_not_capitalized(self, create_first_team):
        data = {
            'name': 'valid Coach',
            'date_of_birth': '1980-01-01',
            'team': reverse('team-detail', args=[create_first_team.id]),
        }

        serializer = CoachSerializer(data=data)
        assert not serializer.is_valid()
        assert 'Name should be capitalized.' in serializer.errors['name']

    @pytest.mark.django_db
    def test_coach_invalid_name_full_caps(self, create_first_team):
        data = {
            'name': 'VALID COACH',
            'date_of_birth': '1980-01-01',
            'team': reverse('team-detail', args=[create_first_team.id]),
        }

        serializer = CoachSerializer(data=data)
        assert not serializer.is_valid()
        assert 'Name should be capitalized.' in serializer.errors['name']

    @pytest.mark.django_db
    def test_coach_invalid_date_of_birth(self, create_first_team):
        data = {
            'name': 'Valid Coach',
            'date_of_birth': date.today() - timedelta(days=(365*17)),
            'team': reverse('team-detail', args=[create_first_team.id]),
        }

        serializer = CoachSerializer(data=data)
        assert not serializer.is_valid()
        assert 'Coach has to be at least 18 years old.' in serializer.errors['date_of_birth']


class TestPlayerSerializer:
    @pytest.mark.django_db
    def test_valid_player_no_stats(self, create_first_team, rf):
        request = rf.get('/dummy-url/')

        data = {
            'name': 'Valid Player',
            'date_of_birth': '1980-01-01',
            'team': reverse('team-detail', args=[create_first_team.id]),
            'country': 'USA',
            'position': 'SF',
            'height': 201,
            'weight': 100,
            'jersey_number': 23,
        }

        serializer = PlayerSerializer(data=data, context={'request': request})
        assert serializer.is_valid()
        assert serializer.save()
        assert serializer.data['name'] == data['name']
        assert reverse('team-detail', args=[create_first_team.id]) in serializer.data['team']
        assert serializer.data['team_name_abbreviation'] == create_first_team.name_abbreviation
        assert serializer.data['date_of_birth'] == data['date_of_birth']
        assert serializer.data['country'] == data['country']
        assert serializer.data['position'] == data['position']
        assert serializer.data['height'] == data['height']
        assert serializer.data['weight'] == data['weight']
        assert serializer.data['jersey_number'] == data['jersey_number']
        assert serializer.data['points_per_game'] == 0.0
        assert serializer.data['offensive_rebounds_per_game'] == 0.0
        assert serializer.data['defensive_rebounds_per_game'] == 0.0
        assert serializer.data['rebounds_per_game'] == 0.0
        assert serializer.data['assists_per_game'] == 0.0
        assert serializer.data['steals_per_game'] == 0.0
        assert serializer.data['blocks_per_game'] == 0.0
        assert serializer.data['turnovers_per_game'] == 0.0
        assert serializer.data['field_goal_percentage'] == 0.0
        assert serializer.data['three_point_field_goal_percentage'] == 0.0
        assert serializer.data['free_throw_percentage'] == 0.0
        assert serializer.data['all_stats'] == f'{serializer.data.get("url")}stats/'

    @pytest.mark.django_db
    def test_valid_player_with_stats(self, create_first_team, create_first_game, create_second_game, rf):
        request = rf.get('/dummy-url/')

        player_data = {
            'name': 'Valid Player',
            'date_of_birth': '1980-01-01',
            'team': reverse('team-detail', args=[create_first_team.id]),
            'country': 'USA',
            'position': 'SF',
            'height': 201,
            'weight': 100,
            'jersey_number': 23,
        }

        serializer = PlayerSerializer(data=player_data, context={'request': request})
        assert serializer.is_valid()
        player = serializer.save()

        first_stats_data = {
            'game': create_first_game,
            'player': player,
            'field_goals_made': 3,
            'field_goals_attempted': 6,
            'three_pointers_made': 1,
            'three_pointers_attempted': 4,
            'free_throws_made': 4,
            'free_throws_attempted': 4,
            'defensive_rebounds': 8,
            'offensive_rebounds': 5,
            'assists': 1,
            'steals': 0,
            'blocks': 4,
            'turnovers': 1,
        }

        second_stats_data = {
            'game': create_second_game,
            'player': player,
            'field_goals_made': 8,
            'field_goals_attempted': 12,
            'three_pointers_made': 4,
            'three_pointers_attempted': 4,
            'free_throws_made': 12,
            'free_throws_attempted': 13,
            'defensive_rebounds': 2,
            'offensive_rebounds': 1,
            'assists': 6,
            'steals': 2,
            'blocks': 0,
            'turnovers': 0,
        }

        Stats.objects.create(**first_stats_data)
        Stats.objects.create(**second_stats_data)

        player.refresh_from_db()

        assert serializer.data['name'] == player_data['name']
        assert reverse('team-detail', args=[create_first_team.id]) in serializer.data['team']
        assert serializer.data['team_name_abbreviation'] == create_first_team.name_abbreviation
        assert serializer.data['date_of_birth'] == player_data['date_of_birth']
        assert serializer.data['country'] == player_data['country']
        assert serializer.data['position'] == player_data['position']
        assert serializer.data['height'] == player_data['height']
        assert serializer.data['weight'] == player_data['weight']
        assert serializer.data['jersey_number'] == player_data['jersey_number']
        assert serializer.data['points_per_game'] == 21.5
        assert serializer.data['offensive_rebounds_per_game'] == 3.0
        assert serializer.data['defensive_rebounds_per_game'] == 5.0
        assert serializer.data['rebounds_per_game'] == 8.0
        assert serializer.data['assists_per_game'] == 3.5
        assert serializer.data['steals_per_game'] == 1.0
        assert serializer.data['blocks_per_game'] == 2.0
        assert serializer.data['turnovers_per_game'] == 0.5
        assert serializer.data['field_goal_percentage'] == 61.11
        assert serializer.data['three_point_field_goal_percentage'] == 62.5
        assert serializer.data['free_throw_percentage'] == 94.12
        assert serializer.data['all_stats'] == f'{serializer.data.get("url")}stats/'

    @pytest.mark.django_db
    def test_player_existing_jersey_number(self, create_first_team, create_first_player):
        data = {
            'name': 'Valid Player',
            'date_of_birth': '1980-01-01',
            'team': reverse('team-detail', args=[create_first_team.id]),
            'country': 'USA',
            'position': 'SF',
            'height': 201,
            'weight': 100,
            'jersey_number': 22,
        }

        serializer = PlayerSerializer(data=data)
        assert not serializer.is_valid()
        assert (
                'This jersey number is already assigned to a player in this team.' in
                serializer.errors['non_field_errors']
        )

    @pytest.mark.django_db
    def test_player_invalid_name_nonletters(self, create_first_team):
        data = {
            'name': 'Va3lid Player',
            'date_of_birth': '1980-01-01',
            'team': reverse('team-detail', args=[create_first_team.id]),
            'country': 'USA',
            'position': 'SF',
            'height': 201,
            'weight': 100,
            'jersey_number': 22,
        }

        serializer = PlayerSerializer(data=data)
        assert not serializer.is_valid()
        assert 'Name should only contain letters.' in serializer.errors['name']

    @pytest.mark.django_db
    def test_player_invalid_name_not_capitalized(self, create_first_team):
        data = {
            'name': 'valid Player',
            'date_of_birth': '1980-01-01',
            'team': reverse('team-detail', args=[create_first_team.id]),
            'country': 'USA',
            'position': 'SF',
            'height': 201,
            'weight': 100,
            'jersey_number': 22,
        }

        serializer = PlayerSerializer(data=data)
        assert not serializer.is_valid()
        assert 'Name should be capitalized.' in serializer.errors['name']

    @pytest.mark.django_db
    def test_player_invalid_name_fully_capitalized(self, create_first_team):
        data = {
            'name': 'VALID PLAYER',
            'date_of_birth': '1980-01-01',
            'team': reverse('team-detail', args=[create_first_team.id]),
            'country': 'USA',
            'position': 'SF',
            'height': 201,
            'weight': 100,
            'jersey_number': 22,
        }

        serializer = PlayerSerializer(data=data)
        assert not serializer.is_valid()
        assert 'Name should be capitalized.' in serializer.errors['name']

    @pytest.mark.django_db
    def test_player_invalid_date_of_birth(self, create_first_team):
        data = {
            'name': 'Valid Player',
            'date_of_birth': date.today() + timedelta(days=1),
            'team': reverse('team-detail', args=[create_first_team.id]),
            'country': 'USA',
            'position': 'SF',
            'height': 201,
            'weight': 100,
            'jersey_number': 22,
        }

        serializer = PlayerSerializer(data=data)
        assert not serializer.is_valid()
        assert 'Birth date cannot be in the future.' in serializer.errors['date_of_birth']

    @pytest.mark.django_db
    def test_player_invalid_country_not_capitalized(self, create_first_team):
        data = {
            'name': 'Valid Player',
            'date_of_birth': '1980-01-01',
            'team': reverse('team-detail', args=[create_first_team.id]),
            'country': 'united kingdom',
            'position': 'SF',
            'height': 201,
            'weight': 100,
            'jersey_number': 22,
        }

        serializer = PlayerSerializer(data=data)
        assert not serializer.is_valid()
        assert 'Country name should be capitalized.' in serializer.errors['country']

    @pytest.mark.django_db
    def test_player_invalid_country_nonletters(self, create_first_team):
        data = {
            'name': 'Valid Player',
            'date_of_birth': '1980-01-01',
            'team': reverse('team-detail', args=[create_first_team.id]),
            'country': 'P0land',
            'position': 'SF',
            'height': 201,
            'weight': 100,
            'jersey_number': 22,
        }

        serializer = PlayerSerializer(data=data)
        assert not serializer.is_valid()
        assert 'Country name should only contain letters.' in serializer.errors['country']

    @pytest.mark.django_db
    def test_player_invalid_height(self, create_first_team):
        data = {
            'name': 'Valid Player',
            'date_of_birth': '1980-01-01',
            'team': reverse('team-detail', args=[create_first_team.id]),
            'country': 'Poland',
            'position': 'SF',
            'height': -5,
            'weight': 100,
            'jersey_number': 22,
        }

        serializer = PlayerSerializer(data=data)
        assert not serializer.is_valid()
        assert 'Height must be greater than 0.' in serializer.errors['height']

    @pytest.mark.django_db
    def test_player_invalid_weight(self, create_first_team):
        data = {
            'name': 'Valid Player',
            'date_of_birth': '1980-01-01',
            'team': reverse('team-detail', args=[create_first_team.id]),
            'country': 'Poland',
            'position': 'SF',
            'height': 200,
            'weight': -5,
            'jersey_number': 22,
        }

        serializer = PlayerSerializer(data=data)
        assert not serializer.is_valid()
        assert 'Weight must be greater than 0.' in serializer.errors['weight']

    @pytest.mark.django_db
    def test_player_invalid_jersey_number_too_high(self, create_first_team):
        data = {
            'name': 'Valid Player',
            'date_of_birth': '1980-01-01',
            'team': reverse('team-detail', args=[create_first_team.id]),
            'country': 'Poland',
            'position': 'SF',
            'height': 200,
            'weight': 100,
            'jersey_number': 100,
        }

        serializer = PlayerSerializer(data=data)
        assert not serializer.is_valid()
        assert 'Invalid jersey number. Only numbers 0-99 are allowed.' in serializer.errors['jersey_number']

    @pytest.mark.django_db
    def test_player_invalid_jersey_number_too_low(self, create_first_team):
        data = {
            'name': 'Valid Player',
            'date_of_birth': '1980-01-01',
            'team': reverse('team-detail', args=[create_first_team.id]),
            'country': 'Poland',
            'position': 'SF',
            'height': 200,
            'weight': 100,
            'jersey_number': -1,
        }

        serializer = PlayerSerializer(data=data)
        assert not serializer.is_valid()
        assert 'Invalid jersey number. Only numbers 0-99 are allowed.' in serializer.errors['jersey_number']


class TestGameSerializer:
    @pytest.mark.django_db
    def test_valid_game(self, create_first_team, create_second_team, create_first_player, create_second_player, rf):
        request = rf.get('/dummy-url/')

        game_data = {
            'date': '2024-01-02 20:00:00',
            'home_team': reverse('team-detail', args=[create_first_team.id]),
            'away_team': reverse('team-detail', args=[create_second_team.id]),
        }

        serializer = GameSerializer(data=game_data, context={'request': request})
        assert serializer.is_valid(), serializer.errors
        game = serializer.save()

        first_stats_data = {
            'game': game,
            'player': create_first_player,
            'field_goals_made': 3,
            'field_goals_attempted': 6,
            'three_pointers_made': 1,
            'three_pointers_attempted': 4,
            'free_throws_made': 4,
            'free_throws_attempted': 4,
            'defensive_rebounds': 8,
            'offensive_rebounds': 5,
            'assists': 1,
            'steals': 0,
            'blocks': 4,
            'turnovers': 1,
        }

        second_stats_data = {
            'game': game,
            'player': create_second_player,
            'field_goals_made': 8,
            'field_goals_attempted': 12,
            'three_pointers_made': 4,
            'three_pointers_attempted': 4,
            'free_throws_made': 12,
            'free_throws_attempted': 13,
            'defensive_rebounds': 2,
            'offensive_rebounds': 1,
            'assists': 6,
            'steals': 2,
            'blocks': 0,
            'turnovers': 0,
        }

        Stats.objects.create(**first_stats_data)
        Stats.objects.create(**second_stats_data)

        game.refresh_from_db()

        assert serializer.data['date'] == '2024-01-02T20:00:00Z'
        assert (
                serializer.data['game_info'] ==
                (
                    f'{create_second_team.name_abbreviation} @ {create_first_team.name_abbreviation} -'
                    f' {game_data["date"]}+00:00'
                )
        )
        assert game_data['home_team'] in serializer.data['home_team']
        assert serializer.data['home_team_name_abbreviation'] == create_first_team.name_abbreviation
        assert game_data['away_team'] in serializer.data['away_team']
        assert serializer.data['away_team_name_abbreviation'] == create_second_team.name_abbreviation
        assert serializer.data['home_team_score'] == 11
        assert serializer.data['away_team_score'] == 32
        assert serializer.data['box_score'] == f'{serializer.data.get("url")}stats/'

    @pytest.mark.django_db
    def test_game_same_team_twice(self, create_first_team):
        data = {
            'date': '2024-01-02 20:00:00',
            'home_team': reverse('team-detail', args=[create_first_team.id]),
            'away_team': reverse('team-detail', args=[create_first_team.id]),
        }

        serializer = GameSerializer(data=data)
        assert not serializer.is_valid()
        assert 'Home team and Away team cannot be the same.' in serializer.errors['non_field_errors']

    @pytest.mark.django_db
    def test_game_between_the_same_teams_twice(self, create_first_team, create_second_team, create_first_game):
        data = {
            'date': '2024-01-01',
            'home_team': reverse('team-detail', args=[create_first_team.id]),
            'away_team': reverse('team-detail', args=[create_second_team.id]),
        }

        serializer = GameSerializer(data=data)
        assert not serializer.is_valid()
        assert 'Cannot have two games between the same teams at the same time.' in serializer.errors['non_field_errors']

    @pytest.mark.django_db
    def test_game_invalid_date_home_team(self, create_first_team, create_third_team, create_first_game):
        data = {
            'date': '2024-01-01 02:00:00',
            'home_team': reverse('team-detail', args=[create_first_team.id]),
            'away_team': reverse('team-detail', args=[create_third_team.id]),
        }

        serializer = GameSerializer(data=data)
        assert not serializer.is_valid()
        assert 'Home team has another game around the same time.' in serializer.errors['non_field_errors']

    @pytest.mark.django_db
    def test_game_invalid_date_away_team(self, create_first_team, create_third_team, create_first_game):
        data = {
            'date': '2024-01-01 02:00:00',
            'home_team': reverse('team-detail', args=[create_third_team.id]),
            'away_team': reverse('team-detail', args=[create_first_team.id]),
        }

        serializer = GameSerializer(data=data)
        assert not serializer.is_valid()
        assert 'Away team has another game around the same time.' in serializer.errors['non_field_errors']


class TestStatsSerializer:
    @pytest.mark.django_db
    def test_valid_stats(self, create_first_game, create_first_player, rf):
        request = rf.get('/dummy-url/')

        data = {
            'game': reverse('game-detail', args=[create_first_game.id]),
            'player': reverse('player-detail', args=[create_first_player.id]),
            'field_goals_made': 3,
            'field_goals_attempted': 6,
            'three_pointers_made': 1,
            'three_pointers_attempted': 4,
            'free_throws_made': 4,
            'free_throws_attempted': 4,
            'defensive_rebounds': 8,
            'offensive_rebounds': 5,
            'assists': 1,
            'steals': 0,
            'blocks': 4,
            'turnovers': 1,
        }

        serializer = StatsSerializer(data=data, context={'request': request})
        assert serializer.is_valid(), serializer.errors
        assert serializer.save()
        assert data['game'] in serializer.data['game']
        assert serializer.data['game_info'] == 'GSW @ MIA - 2024-01-01 00:00:00+00:00'
        assert data['player'] in serializer.data['player']
        assert serializer.data['player_name'] == create_first_player.name
        assert serializer.data['field_goals_made'] == data['field_goals_made']
        assert serializer.data['field_goals_attempted'] == data['field_goals_attempted']
        assert serializer.data['field_goal_percentage'] == 50.0
        assert serializer.data['three_pointers_made'] == data['three_pointers_made']
        assert serializer.data['three_point_percentage'] == 25.0
        assert serializer.data['free_throws_made'] == data['free_throws_made']
        assert serializer.data['free_throws_attempted'] == data['free_throws_attempted']
        assert serializer.data['free_throw_percentage'] == 100.0
        assert serializer.data['offensive_rebounds'] == data['offensive_rebounds']
        assert serializer.data['defensive_rebounds'] == data['defensive_rebounds']
        assert serializer.data['rebounds'] == data['defensive_rebounds'] + data['offensive_rebounds']
        assert serializer.data['assists'] == data['assists']
        assert serializer.data['steals'] == data['steals']
        assert serializer.data['blocks'] == data['blocks']
        assert serializer.data['turnovers'] == data['turnovers']

    @pytest.mark.django_db
    def test_valid_stats_no_attempts(self, create_first_game, create_first_player, rf):
        request = rf.get('/dummy-url/')

        data = {
            'game': reverse('game-detail', args=[create_first_game.id]),
            'player': reverse('player-detail', args=[create_first_player.id]),
            'field_goals_made': 0,
            'field_goals_attempted': 0,
            'three_pointers_made': 0,
            'three_pointers_attempted': 0,
            'free_throws_made': 0,
            'free_throws_attempted': 0,
            'defensive_rebounds': 8,
            'offensive_rebounds': 5,
            'assists': 1,
            'steals': 0,
            'blocks': 4,
            'turnovers': 1,
        }

        serializer = StatsSerializer(data=data, context={'request': request})
        assert serializer.is_valid()
        assert serializer.save()
        assert data['game'] in serializer.data['game']
        assert serializer.data['game_info'] == 'GSW @ MIA - 2024-01-01 00:00:00+00:00'
        assert data['player'] in serializer.data['player']
        assert serializer.data['player_name'] == create_first_player.name
        assert serializer.data['field_goals_made'] == data['field_goals_made']
        assert serializer.data['field_goals_attempted'] == data['field_goals_attempted']
        assert serializer.data['field_goal_percentage'] == 0.0
        assert serializer.data['three_pointers_made'] == data['three_pointers_made']
        assert serializer.data['three_point_percentage'] == 0.0
        assert serializer.data['free_throws_made'] == data['free_throws_made']
        assert serializer.data['free_throws_attempted'] == data['free_throws_attempted']
        assert serializer.data['free_throw_percentage'] == 0.0
        assert serializer.data['offensive_rebounds'] == data['offensive_rebounds']
        assert serializer.data['defensive_rebounds'] == data['defensive_rebounds']
        assert serializer.data['rebounds'] == data['defensive_rebounds'] + data['offensive_rebounds']
        assert serializer.data['assists'] == data['assists']
        assert serializer.data['steals'] == data['steals']
        assert serializer.data['blocks'] == data['blocks']
        assert serializer.data['turnovers'] == data['turnovers']

    @pytest.mark.django_db
    def test_stats_same_player_twice(self, create_first_game, create_first_player, create_first_statline):
        data = {
            'game': reverse('game-detail', args=[create_first_game.id]),
            'player': reverse('player-detail', args=[create_first_player.id]),
            'field_goals_made': 3,
            'field_goals_attempted': 6,
            'three_pointers_made': 1,
            'three_pointers_attempted': 4,
            'free_throws_made': 4,
            'free_throws_attempted': 4,
            'defensive_rebounds': 8,
            'offensive_rebounds': 5,
            'assists': 1,
            'steals': 0,
            'blocks': 4,
            'turnovers': 1,
        }

        serializer = StatsSerializer(data=data)
        assert not serializer.is_valid()
        assert (
                'Cannot have two instances of stats of the same player in one game.' in
                serializer.errors['non_field_errors']
        )

    @pytest.mark.django_db
    def test_stats_same_player_twice(self, create_first_game, create_third_player):
        data = {
            'game': reverse('game-detail', args=[create_first_game.id]),
            'player': reverse('player-detail', args=[create_third_player.id]),
            'field_goals_made': 3,
            'field_goals_attempted': 6,
            'three_pointers_made': 1,
            'three_pointers_attempted': 4,
            'free_throws_made': 4,
            'free_throws_attempted': 4,
            'defensive_rebounds': 8,
            'offensive_rebounds': 5,
            'assists': 1,
            'steals': 0,
            'blocks': 4,
            'turnovers': 1,
        }

        serializer = StatsSerializer(data=data)
        assert not serializer.is_valid()
        assert 'This player is not in the team participating in the game.' in serializer.errors['non_field_errors']

    @pytest.mark.django_db
    def test_stats_invalid_more_fgm_than_fga(self, create_first_game, create_first_player):
        data = {
            'game': reverse('game-detail', args=[create_first_game.id]),
            'player': reverse('player-detail', args=[create_first_player.id]),
            'field_goals_made': 7,
            'field_goals_attempted': 6,
            'three_pointers_made': 1,
            'three_pointers_attempted': 4,
            'free_throws_made': 4,
            'free_throws_attempted': 4,
            'defensive_rebounds': 8,
            'offensive_rebounds': 5,
            'assists': 1,
            'steals': 0,
            'blocks': 4,
            'turnovers': 1,
        }

        serializer = StatsSerializer(data=data)
        assert not serializer.is_valid()
        assert (
                "The number of shots made can't be greater than the number of shots attempted." in
                serializer.errors['non_field_errors']
        )

    @pytest.mark.django_db
    def test_stats_invalid_more_tpm_than_tpa(self, create_first_game, create_first_player):
        data = {
            'game': reverse('game-detail', args=[create_first_game.id]),
            'player': reverse('player-detail', args=[create_first_player.id]),
            'field_goals_made': 6,
            'field_goals_attempted': 6,
            'three_pointers_made': 5,
            'three_pointers_attempted': 4,
            'free_throws_made': 4,
            'free_throws_attempted': 4,
            'defensive_rebounds': 8,
            'offensive_rebounds': 5,
            'assists': 1,
            'steals': 0,
            'blocks': 4,
            'turnovers': 1,
        }

        serializer = StatsSerializer(data=data)
        assert not serializer.is_valid()
        assert (
                "The number of shots made can't be greater than the number of shots attempted." in
                serializer.errors['non_field_errors']
        )

    @pytest.mark.django_db
    def test_stats_invalid_more_ftm_than_fta(self, create_first_game, create_first_player):
        data = {
            'game': reverse('game-detail', args=[create_first_game.id]),
            'player': reverse('player-detail', args=[create_first_player.id]),
            'field_goals_made': 5,
            'field_goals_attempted': 6,
            'three_pointers_made': 1,
            'three_pointers_attempted': 4,
            'free_throws_made': 5,
            'free_throws_attempted': 4,
            'defensive_rebounds': 8,
            'offensive_rebounds': 5,
            'assists': 1,
            'steals': 0,
            'blocks': 4,
            'turnovers': 1,
        }

        serializer = StatsSerializer(data=data)
        assert not serializer.is_valid()
        assert (
                "The number of shots made can't be greater than the number of shots attempted." in
                serializer.errors['non_field_errors']
        )

    @pytest.mark.django_db
    def test_stats_invalid_more_tpa_than_fga(self, create_first_game, create_first_player):
        data = {
            'game': reverse('game-detail', args=[create_first_game.id]),
            'player': reverse('player-detail', args=[create_first_player.id]),
            'field_goals_made': 5,
            'field_goals_attempted': 6,
            'three_pointers_made': 1,
            'three_pointers_attempted': 7,
            'free_throws_made': 4,
            'free_throws_attempted': 4,
            'defensive_rebounds': 8,
            'offensive_rebounds': 5,
            'assists': 1,
            'steals': 0,
            'blocks': 4,
            'turnovers': 1,
        }

        serializer = StatsSerializer(data=data)
        assert not serializer.is_valid()
        assert (
                "The number of three pointers attempted can't be greater than the number of field goals attempted." in
                serializer.errors['non_field_errors']
        )

    @pytest.mark.django_db
    def test_stats_invalid_more_tpm_than_fgm(self, create_first_game, create_first_player):
        data = {
            'game': reverse('game-detail', args=[create_first_game.id]),
            'player': reverse('player-detail', args=[create_first_player.id]),
            'field_goals_made': 3,
            'field_goals_attempted': 6,
            'three_pointers_made': 4,
            'three_pointers_attempted': 4,
            'free_throws_made': 4,
            'free_throws_attempted': 4,
            'defensive_rebounds': 8,
            'offensive_rebounds': 5,
            'assists': 1,
            'steals': 0,
            'blocks': 4,
            'turnovers': 1,
        }

        serializer = StatsSerializer(data=data)
        assert not serializer.is_valid()
        assert (
                "The number of three pointers made can't be greater than the number of field goals made." in
                serializer.errors['non_field_errors']
        )

    @pytest.mark.django_db
    def test_stats_invalid_field_goals_made_negative(self, create_first_game, create_first_player):
        data = {
            'game': reverse('game-detail', args=[create_first_game.id]),
            'player': reverse('player-detail', args=[create_first_player.id]),
            'field_goals_made': -1,
            'field_goals_attempted': 6,
            'three_pointers_made': 4,
            'three_pointers_attempted': 4,
            'free_throws_made': 4,
            'free_throws_attempted': 4,
            'defensive_rebounds': 8,
            'offensive_rebounds': 5,
            'assists': 1,
            'steals': 0,
            'blocks': 4,
            'turnovers': 1,
        }

        serializer = StatsSerializer(data=data)
        assert not serializer.is_valid()
        assert 'The number of field goals made has to be non-negative.' in serializer.errors['field_goals_made']

    @pytest.mark.django_db
    def test_stats_invalid_field_goals_attempted_negative(self, create_first_game, create_first_player):
        data = {
            'game': reverse('game-detail', args=[create_first_game.id]),
            'player': reverse('player-detail', args=[create_first_player.id]),
            'field_goals_made': 6,
            'field_goals_attempted': -1,
            'three_pointers_made': 4,
            'three_pointers_attempted': 4,
            'free_throws_made': 4,
            'free_throws_attempted': 4,
            'defensive_rebounds': 8,
            'offensive_rebounds': 5,
            'assists': 1,
            'steals': 0,
            'blocks': 4,
            'turnovers': 1,
        }

        serializer = StatsSerializer(data=data)
        assert not serializer.is_valid()
        assert (
                'The number of field goals attempted has to be non-negative.' in
                serializer.errors['field_goals_attempted']
        )

    @pytest.mark.django_db
    def test_stats_invalid_three_pointers_made_negative(self, create_first_game, create_first_player):
        data = {
            'game': reverse('game-detail', args=[create_first_game.id]),
            'player': reverse('player-detail', args=[create_first_player.id]),
            'field_goals_made': 6,
            'field_goals_attempted': 6,
            'three_pointers_made': -4,
            'three_pointers_attempted': 4,
            'free_throws_made': 4,
            'free_throws_attempted': 4,
            'defensive_rebounds': 8,
            'offensive_rebounds': 5,
            'assists': 1,
            'steals': 0,
            'blocks': 4,
            'turnovers': 1,
        }

        serializer = StatsSerializer(data=data)
        assert not serializer.is_valid()
        assert 'The number of three pointers made has to be non-negative.' in serializer.errors['three_pointers_made']

    @pytest.mark.django_db
    def test_stats_invalid_three_pointers_attempted_negative(self, create_first_game, create_first_player):
        data = {
            'game': reverse('game-detail', args=[create_first_game.id]),
            'player': reverse('player-detail', args=[create_first_player.id]),
            'field_goals_made': 6,
            'field_goals_attempted': 6,
            'three_pointers_made': 4,
            'three_pointers_attempted': -4,
            'free_throws_made': 4,
            'free_throws_attempted': 4,
            'defensive_rebounds': 8,
            'offensive_rebounds': 5,
            'assists': 1,
            'steals': 0,
            'blocks': 4,
            'turnovers': 1,
        }

        serializer = StatsSerializer(data=data)
        assert not serializer.is_valid()
        assert (
                'The number of three pointers attempted has to be non-negative.' in
                serializer.errors['three_pointers_attempted']
        )

    @pytest.mark.django_db
    def test_stats_invalid_free_throws_made_negative(self, create_first_game, create_first_player):
        data = {
            'game': reverse('game-detail', args=[create_first_game.id]),
            'player': reverse('player-detail', args=[create_first_player.id]),
            'field_goals_made': 6,
            'field_goals_attempted': 6,
            'three_pointers_made': 4,
            'three_pointers_attempted': 4,
            'free_throws_made': -4,
            'free_throws_attempted': 4,
            'defensive_rebounds': 8,
            'offensive_rebounds': 5,
            'assists': 1,
            'steals': 0,
            'blocks': 4,
            'turnovers': 1,
        }

        serializer = StatsSerializer(data=data)
        assert not serializer.is_valid()
        assert 'The number of free throws made has to be non-negative.' in serializer.errors['free_throws_made']

    @pytest.mark.django_db
    def test_stats_invalid_free_throws_attempted_negative(self, create_first_game, create_first_player):
        data = {
            'game': reverse('game-detail', args=[create_first_game.id]),
            'player': reverse('player-detail', args=[create_first_player.id]),
            'field_goals_made': 6,
            'field_goals_attempted': 6,
            'three_pointers_made': 4,
            'three_pointers_attempted': 4,
            'free_throws_made': 4,
            'free_throws_attempted': -4,
            'defensive_rebounds': 8,
            'offensive_rebounds': 5,
            'assists': 1,
            'steals': 0,
            'blocks': 4,
            'turnovers': 1,
        }

        serializer = StatsSerializer(data=data)
        assert not serializer.is_valid()
        assert (
                'The number of free throws attempted has to be non-negative.' in
                serializer.errors['free_throws_attempted']
        )

    @pytest.mark.django_db
    def test_stats_invalid_defensive_rebounds_negative(self, create_first_game, create_first_player):
        data = {
            'game': reverse('game-detail', args=[create_first_game.id]),
            'player': reverse('player-detail', args=[create_first_player.id]),
            'field_goals_made': 6,
            'field_goals_attempted': 6,
            'three_pointers_made': 4,
            'three_pointers_attempted': 4,
            'free_throws_made': 4,
            'free_throws_attempted': 4,
            'defensive_rebounds': -8,
            'offensive_rebounds': 5,
            'assists': 1,
            'steals': 0,
            'blocks': 4,
            'turnovers': 1,
        }

        serializer = StatsSerializer(data=data)
        assert not serializer.is_valid()
        assert 'The number of defensive rebounds has to be non-negative.' in serializer.errors['defensive_rebounds']

    @pytest.mark.django_db
    def test_stats_invalid_offensive_rebounds_negative(self, create_first_game, create_first_player):
        data = {
            'game': reverse('game-detail', args=[create_first_game.id]),
            'player': reverse('player-detail', args=[create_first_player.id]),
            'field_goals_made': 6,
            'field_goals_attempted': 6,
            'three_pointers_made': 4,
            'three_pointers_attempted': 4,
            'free_throws_made': 4,
            'free_throws_attempted': 4,
            'defensive_rebounds': 8,
            'offensive_rebounds': -5,
            'assists': 1,
            'steals': 0,
            'blocks': 4,
            'turnovers': 1,
        }

        serializer = StatsSerializer(data=data)
        assert not serializer.is_valid()
        assert 'The number of offensive rebounds has to be non-negative.' in serializer.errors['offensive_rebounds']

    @pytest.mark.django_db
    def test_stats_invalid_assists_negative(self, create_first_game, create_first_player):
        data = {
            'game': reverse('game-detail', args=[create_first_game.id]),
            'player': reverse('player-detail', args=[create_first_player.id]),
            'field_goals_made': 6,
            'field_goals_attempted': 6,
            'three_pointers_made': 4,
            'three_pointers_attempted': 4,
            'free_throws_made': 4,
            'free_throws_attempted': 4,
            'defensive_rebounds': 8,
            'offensive_rebounds': 5,
            'assists': -1,
            'steals': 0,
            'blocks': 4,
            'turnovers': 1,
        }

        serializer = StatsSerializer(data=data)
        assert not serializer.is_valid()
        assert 'The number of assists has to be non-negative.' in serializer.errors['assists']

    @pytest.mark.django_db
    def test_stats_invalid_steals_negative(self, create_first_game, create_first_player):
        data = {
            'game': reverse('game-detail', args=[create_first_game.id]),
            'player': reverse('player-detail', args=[create_first_player.id]),
            'field_goals_made': 6,
            'field_goals_attempted': 6,
            'three_pointers_made': 4,
            'three_pointers_attempted': 4,
            'free_throws_made': 4,
            'free_throws_attempted': 4,
            'defensive_rebounds': 8,
            'offensive_rebounds': 5,
            'assists': 1,
            'steals': -10,
            'blocks': 4,
            'turnovers': 1,
        }

        serializer = StatsSerializer(data=data)
        assert not serializer.is_valid()
        assert 'The number of steals has to be non-negative.' in serializer.errors['steals']

    @pytest.mark.django_db
    def test_stats_invalid_blocks_negative(self, create_first_game, create_first_player):
        data = {
            'game': reverse('game-detail', args=[create_first_game.id]),
            'player': reverse('player-detail', args=[create_first_player.id]),
            'field_goals_made': 6,
            'field_goals_attempted': 6,
            'three_pointers_made': 4,
            'three_pointers_attempted': 4,
            'free_throws_made': 4,
            'free_throws_attempted': 4,
            'defensive_rebounds': 8,
            'offensive_rebounds': 5,
            'assists': 1,
            'steals': 10,
            'blocks': -4,
            'turnovers': 1,
        }

        serializer = StatsSerializer(data=data)
        assert not serializer.is_valid()
        assert 'The number of blocks has to be non-negative.' in serializer.errors['blocks']

    @pytest.mark.django_db
    def test_stats_invalid_turnovers_negative(self, create_first_game, create_first_player):
        data = {
            'game': reverse('game-detail', args=[create_first_game.id]),
            'player': reverse('player-detail', args=[create_first_player.id]),
            'field_goals_made': 6,
            'field_goals_attempted': 6,
            'three_pointers_made': 4,
            'three_pointers_attempted': 4,
            'free_throws_made': 4,
            'free_throws_attempted': 4,
            'defensive_rebounds': 8,
            'offensive_rebounds': 5,
            'assists': 1,
            'steals': 10,
            'blocks': 4,
            'turnovers': -1,
        }

        serializer = StatsSerializer(data=data)
        assert not serializer.is_valid()
        assert 'The number of turnovers has to be non-negative.' in serializer.errors['turnovers']
