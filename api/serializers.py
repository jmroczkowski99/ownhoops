from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.db import models
from django.db.models import Q
from django.urls import reverse
from drf_spectacular.utils import extend_schema_field, extend_schema_serializer, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from api.models import Team, Coach, Player, Game, Stats
from api.validators import (
    validate_alpha_and_title,
    validate_future_date,
    validate_positive,
    validate_over_eighteen,
    validate_nonnegative,
    validate_title_or_number_start,
)
import datetime


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Example Team',
            summary='An example team',
            value={
                "url": "http://127.0.0.1:8000/teams/1/",
                "id": 1,
                "name_abbreviation": "MIA",
                "full_name": "Miami Heat",
                "coach": {
                    "url": "http://127.0.0.1:8000/coaches/1/",
                    "id": 1,
                    "name": "Erik Spoelstra"
                },
                "players": [
                    {
                        "url": "http://127.0.0.1:8000/players/2/",
                        "id": 2,
                        "name": "Jimmy Butler",
                        "position": "SF",
                        "jersey_number": 22
                    },
                    {
                        "url": "http://127.0.0.1:8000/players/3/",
                        "id": 3,
                        "name": "Bam Adebayo",
                        "position": "C",
                        "jersey_number": 13
                    }
                ],
                "games": [
                    {
                        "url": "http://127.0.0.1:8000/games/1/",
                        "id": 1,
                        "info": "IND @ MIA - 2024-02-26T20:00:00Z",
                        "box_score": "http://127.0.0.1:8000/games/1/stats/"
                    },
                    {
                        "url": "http://127.0.0.1:8000/games/3/",
                        "id": 3,
                        "info": "MIA @ GSW - 2024-02-22T20:00:00Z",
                        "box_score": "http://127.0.0.1:8000/games/3/stats/"
                    }
                ]
            }
        )
    ]
)
class TeamSerializer(serializers.HyperlinkedModelSerializer):
    players = serializers.SerializerMethodField()
    coach = serializers.SerializerMethodField()
    games = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['url', 'id', 'name_abbreviation', 'full_name', 'coach', 'players', 'games']

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_coach(self, obj):
        coach_instance = obj.coach.first()
        coach_data = CoachSerializer(coach_instance, context=self.context).data
        return {
            'url': coach_data.get('url', None),
            'id': coach_data.get('id', None),
            'name': coach_data.get('name', None),
        }

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_players(self, obj):
        players_queryset = obj.players.all()
        players_data = PlayerSerializer(players_queryset, many=True, context=self.context).data
        return [
            {
                'url': player_data.get('url', None),
                'id': player_data.get('id', None),
                'name': player_data.get('name', None),
                'position': player_data.get('position', None),
                'jersey_number': player_data.get('jersey_number', None)
            }
            for player_data in players_data
        ]

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_games(self, obj):
        games_queryset = obj.home_games.all() | obj.away_games.all()
        games_data = GameSerializer(games_queryset, many=True, context=self.context).data
        return [
            {
                'url': game_data.get('url', None),
                'id': game_data.get('id', None),
                'info': (
                    f'{game_data.get("away_team_name_abbreviation", None)} @ '
                    f'{game_data.get("home_team_name_abbreviation", None)} - '
                    f'{game_data.get("date", None)}'
                ),
                'box_score': game_data.get('box_score', None),
            }
            for game_data in games_data
        ]

    def validate_name_abbreviation(self, value):
        if not len(value) == 3:
            raise serializers.ValidationError('Team name abbreviation must contain 3 letters.')

        if not value.replace(' ', '').isalpha():
            raise serializers.ValidationError('Team name abbreviation can contain only letters.')

        if not value.isupper():
            raise serializers.ValidationError('Team name abbreviation should be uppercase.')

        return value

    def validate_full_name(self, value):
        if not value.replace(' ', '').isalnum():
            raise serializers.ValidationError('Team name can contain only letters and numbers.')

        validate_title_or_number_start(value, 'Team name should be capitalized.')

        return value


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Example Coach',
            summary='An example coach',
            value={
                "url": "http://127.0.0.1:8000/coaches/1/",
                "id": 1,
                "name": "Erik Spoelstra",
                "date_of_birth": "1970-01-01",
                "team": "http://127.0.0.1:8000/teams/1/",
                "team_name_abbreviation": "MIA"
            }
        )
    ]
)
class CoachSerializer(serializers.HyperlinkedModelSerializer):
    team_name_abbreviation = serializers.ReadOnlyField(source='team.name_abbreviation')

    class Meta:
        model = Coach
        fields = ['url', 'id', 'name', 'date_of_birth', 'team', 'team_name_abbreviation']

    def validate(self, data):
        team = data.get('team')

        if team:
            existing_coach_query = Coach.objects.filter(team=team)

            if self.instance:
                existing_coach_query = existing_coach_query.exclude(pk=self.instance.pk)

            if existing_coach_query.exists():
                raise serializers.ValidationError('This team already has a coach.')

        return data

    def validate_name(self, value):
        return validate_alpha_and_title(value, 'Name should only contain letters.', 'Name should be capitalized.')

    def validate_date_of_birth(self, value):
        return validate_over_eighteen(value, 'Coach has to be at least 18 years old.')


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Example Player',
            summary='An example player',
            value={
                "url": "http://127.0.0.1:8000/players/1/",
                "id": 1,
                "name": "Stephen Curry",
                "team": "http://127.0.0.1:8000/teams/3/",
                "team_name_abbreviation": "GSW",
                "date_of_birth": "1988-01-01",
                "country": "USA",
                "position": "PG",
                "height": 188,
                "weight": 90,
                "jersey_number": 30,
                "points_per_game": 36,
                "offensive_rebounds_per_game": 0,
                "defensive_rebounds_per_game": 2,
                "rebounds_per_game": 2,
                "assists_per_game": 5,
                "steals_per_game": 0,
                "blocks_per_game": 0,
                "turnovers_per_game": 1,
                "field_goal_percentage": 60.87,
                "three_point_field_goal_percentage": 46.15,
                "free_throw_percentage": 100,
                "all_stats": "http://127.0.0.1:8000/players/1/stats/"
            }
        )
    ]
)
class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    team_name_abbreviation = serializers.ReadOnlyField(source='team.name_abbreviation')
    points_per_game = serializers.SerializerMethodField()
    offensive_rebounds_per_game = serializers.SerializerMethodField()
    defensive_rebounds_per_game = serializers.SerializerMethodField()
    rebounds_per_game = serializers.SerializerMethodField()
    assists_per_game = serializers.SerializerMethodField()
    steals_per_game = serializers.SerializerMethodField()
    blocks_per_game = serializers.SerializerMethodField()
    turnovers_per_game = serializers.SerializerMethodField()
    field_goal_percentage = serializers.SerializerMethodField()
    three_point_field_goal_percentage = serializers.SerializerMethodField()
    free_throw_percentage = serializers.SerializerMethodField()
    all_stats = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = [
            'url',
            'id',
            'name',
            'team',
            'team_name_abbreviation',
            'date_of_birth',
            'country',
            'position',
            'height',
            'weight',
            'jersey_number',
            'points_per_game',
            'offensive_rebounds_per_game',
            'defensive_rebounds_per_game',
            'rebounds_per_game',
            'assists_per_game',
            'steals_per_game',
            'blocks_per_game',
            'turnovers_per_game',
            'field_goal_percentage',
            'three_point_field_goal_percentage',
            'free_throw_percentage',
            'all_stats',
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=Player.objects.all(),
                fields=['jersey_number', 'team'],
                message='This jersey number is already assigned to a player in this team.'
            )
        ]

    def calculate_stat_per_game(self, obj, stat_name):
        player_stats = Stats.objects.filter(player=obj, player__team=obj.team)
        total_stat = sum(
            StatsSerializer(stats, context=self.context).data.get(stat_name, 0)
            for stats in player_stats
        )
        number_of_games = player_stats.count()

        if number_of_games == 0:
            return 0.0
        else:
            return round(total_stat/number_of_games, 2)

    def calculate_stat_percentage(self, obj, stat_name_made, stat_name_attempts):
        player_stats = Stats.objects.filter(player=obj, player__team=obj.team)
        stat_made = sum(
            StatsSerializer(stats, context=self.context).data.get(stat_name_made, 0)
            for stats in player_stats
        )
        stat_attempted = sum(
            StatsSerializer(stats, context=self.context).data.get(stat_name_attempts, 0)
            for stats in player_stats
        )

        if stat_attempted == 0:
            return 0.0
        else:
            return round((stat_made/stat_attempted) * 100, 2)

    @extend_schema_field(OpenApiTypes.FLOAT)
    def get_points_per_game(self, obj):
        return self.calculate_stat_per_game(obj, 'points')

    @extend_schema_field(OpenApiTypes.FLOAT)
    def get_offensive_rebounds_per_game(self, obj):
        return self.calculate_stat_per_game(obj, 'offensive_rebounds')

    @extend_schema_field(OpenApiTypes.FLOAT)
    def get_defensive_rebounds_per_game(self, obj):
        return self.calculate_stat_per_game(obj, 'defensive_rebounds')

    @extend_schema_field(OpenApiTypes.FLOAT)
    def get_rebounds_per_game(self, obj):
        return self.calculate_stat_per_game(obj, 'rebounds')

    @extend_schema_field(OpenApiTypes.FLOAT)
    def get_assists_per_game(self, obj):
        return self.calculate_stat_per_game(obj, 'assists')

    @extend_schema_field(OpenApiTypes.FLOAT)
    def get_steals_per_game(self, obj):
        return self.calculate_stat_per_game(obj, 'steals')

    @extend_schema_field(OpenApiTypes.FLOAT)
    def get_blocks_per_game(self, obj):
        return self.calculate_stat_per_game(obj, 'blocks')

    @extend_schema_field(OpenApiTypes.FLOAT)
    def get_turnovers_per_game(self, obj):
        return self.calculate_stat_per_game(obj, 'turnovers')

    @extend_schema_field(OpenApiTypes.FLOAT)
    def get_field_goal_percentage(self, obj):
        return self.calculate_stat_percentage(obj, 'field_goals_made', 'field_goals_attempted')

    @extend_schema_field(OpenApiTypes.FLOAT)
    def get_three_point_field_goal_percentage(self, obj):
        return self.calculate_stat_percentage(obj, 'three_pointers_made', 'three_pointers_attempted')

    @extend_schema_field(OpenApiTypes.FLOAT)
    def get_free_throw_percentage(self, obj):
        return self.calculate_stat_percentage(obj, 'free_throws_made', 'free_throws_attempted')

    @extend_schema_field(OpenApiTypes.STR)
    def get_all_stats(self, obj):
        stats_url = reverse('player-detail', args=[obj.id]) + 'stats/'
        return self.context['request'].build_absolute_uri(stats_url)

    def validate_name(self, value):
        return validate_alpha_and_title(value, 'Name should only contain letters.', 'Name should be capitalized.')

    def validate_date_of_birth(self, value):
        return validate_future_date(value, 'Birth date cannot be in the future.')

    def validate_country(self, value):
        allowed_uppercase = ['USA', 'DRC']
        return validate_alpha_and_title(
            value,
            'Country name should only contain letters.',
            'Country name should be capitalized.',
            allowed_uppercase,
        )

    def validate_height(self, value):
        return validate_positive(value, 'Height must be greater than 0.')

    def validate_weight(self, value):
        return validate_positive(value, 'Weight must be greater than 0.')

    def validate_jersey_number(self, value):
        if not 0 <= value <= 99:
            raise serializers.ValidationError('Invalid jersey number. Only numbers 0-99 are allowed.')
        
        return value


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Example Game',
            summary='An example game',
            value={
                "url": "http://127.0.0.1:8000/games/1/",
                "id": 1,
                "date": "2024-02-26T20:00:00Z",
                "game_info": "IND @ MIA - 2024-02-26 20:00:00+00:00",
                "home_team": "http://127.0.0.1:8000/teams/1/",
                "home_team_name_abbreviation": "MIA",
                "away_team": "http://127.0.0.1:8000/teams/2/",
                "away_team_name_abbreviation": "IND",
                "home_team_score": 36,
                "away_team_score": 29,
                "box_score": "http://127.0.0.1:8000/games/1/stats/"
            }
        )
    ]
)
class GameSerializer(serializers.HyperlinkedModelSerializer):
    game_info = serializers.SerializerMethodField()
    home_team_name_abbreviation = serializers.ReadOnlyField(source='home_team.name_abbreviation')
    away_team_name_abbreviation = serializers.ReadOnlyField(source='away_team.name_abbreviation')
    home_team_score = serializers.SerializerMethodField()
    away_team_score = serializers.SerializerMethodField()
    box_score = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = [
            'url',
            'id',
            'date',
            'game_info',
            'home_team',
            'home_team_name_abbreviation',
            'away_team',
            'away_team_name_abbreviation',
            'home_team_score',
            'away_team_score',
            'box_score',
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_game_info(self, obj):
        away_team = obj.away_team.name_abbreviation
        home_team = obj.home_team.name_abbreviation
        game_date = obj.date
        return f'{away_team} @ {home_team} - {game_date}'

    @extend_schema_field(OpenApiTypes.INT)
    def get_home_team_score(self, obj):
        home_team_stats = Stats.objects.filter(game=obj, player__team=obj.home_team)
        total_points = sum(
            StatsSerializer(stats, context=self.context).data.get('points', 0)
            for stats in home_team_stats
        )
        return total_points

    @extend_schema_field(OpenApiTypes.INT)
    def get_away_team_score(self, obj):
        away_team_stats = Stats.objects.filter(game=obj, player__team=obj.away_team)
        total_points = sum(
            StatsSerializer(stats, context=self.context).data.get('points', 0)
            for stats in away_team_stats
        )
        return total_points

    @extend_schema_field(OpenApiTypes.STR)
    def get_box_score(self, obj):
        stats_url = reverse('game-detail', args=[obj.id]) + 'stats/'
        return self.context['request'].build_absolute_uri(stats_url)

    def validate(self, data):
        home_team = data['home_team']
        away_team = data['away_team']
        date = data['date']

        if home_team == away_team:
            raise serializers.ValidationError('Home team and Away team cannot be the same.')

        if Game.objects.filter(
            (models.Q(home_team=home_team, away_team=away_team) |
             models.Q(home_team=away_team, away_team=home_team)),
            date=date
        ).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError('Cannot have two games between the same teams at the same time.')

        if Game.objects.filter(
            (Q(home_team=home_team, date__gte=date - datetime.timedelta(hours=2)) &
                Q(home_team=home_team, date__lte=date + datetime.timedelta(hours=2))) |
            (Q(away_team=home_team, date__gte=date - datetime.timedelta(hours=2)) &
                Q(away_team=home_team, date__lte=date + datetime.timedelta(hours=2)))
        ).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError('Home team has another game around the same time.')

        if Game.objects.filter(
            (Q(away_team=away_team, date__gte=date - datetime.timedelta(hours=2)) &
                Q(away_team=away_team, date__lte=date + datetime.timedelta(hours=2))) |
            (Q(home_team=away_team, date__gte=date - datetime.timedelta(hours=2)) &
                Q(home_team=away_team, date__lte=date + datetime.timedelta(hours=2)))
        ).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError('Away team has another game around the same time.')

        return data


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Example Stats',
            summary='An example statline',
            value={
                "url": "http://127.0.0.1:8000/stats/1/",
                "id": 1,
                "game": "http://127.0.0.1:8000/games/1/",
                "game_info": "IND @ MIA - 2024-02-26 20:00:00+00:00",
                "player": "http://127.0.0.1:8000/players/4/",
                "player_name": "Tyrese Haliburton",
                "field_goals_made": 10,
                "field_goals_attempted": 20,
                "field_goal_percentage": 50,
                "three_pointers_made": 5,
                "three_pointers_attempted": 9,
                "three_point_percentage": 55.56,
                "free_throws_made": 4,
                "free_throws_attempted": 4,
                "free_throw_percentage": 100,
                "offensive_rebounds": 1,
                "defensive_rebounds": 3,
                "rebounds": 4,
                "assists": 8,
                "steals": 2,
                "blocks": 0,
                "turnovers": 0,
                "points": 29
            }
        )
    ]
)
class StatsSerializer(serializers.HyperlinkedModelSerializer):
    game_info = serializers.SerializerMethodField()
    player_name = serializers.ReadOnlyField(source='player.name')
    field_goal_percentage = serializers.SerializerMethodField()
    three_point_percentage = serializers.SerializerMethodField()
    free_throw_percentage = serializers.SerializerMethodField()
    points = serializers.SerializerMethodField()
    rebounds = serializers.SerializerMethodField()

    class Meta:
        model = Stats
        fields = [
            'url',
            'id',
            'game',
            'game_info',
            'player',
            'player_name',
            'field_goals_made',
            'field_goals_attempted',
            'field_goal_percentage',
            'three_pointers_made',
            'three_pointers_attempted',
            'three_point_percentage',
            'free_throws_made',
            'free_throws_attempted',
            'free_throw_percentage',
            'offensive_rebounds',
            'defensive_rebounds',
            'rebounds',
            'assists',
            'steals',
            'blocks',
            'turnovers',
            'points',
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_game_info(self, obj):
        away_team = obj.game.away_team.name_abbreviation
        home_team = obj.game.home_team.name_abbreviation
        game_date = obj.game.date
        return f'{away_team} @ {home_team} - {game_date}'

    @extend_schema_field(OpenApiTypes.INT)
    def get_points(self, obj):
        one_pointers = obj.free_throws_made
        two_pointers = obj.field_goals_made - obj.three_pointers_made
        three_pointers = obj.three_pointers_made
        return one_pointers + (two_pointers*2) + (three_pointers*3)

    @extend_schema_field(OpenApiTypes.INT)
    def get_rebounds(self, obj):
        return obj.offensive_rebounds + obj.defensive_rebounds

    @extend_schema_field(OpenApiTypes.FLOAT)
    def get_field_goal_percentage(self, obj):
        if obj.field_goals_attempted == 0:
            return 0
        else:
            return round((obj.field_goals_made/obj.field_goals_attempted) * 100, 2)

    @extend_schema_field(OpenApiTypes.FLOAT)
    def get_three_point_percentage(self, obj):
        if obj.three_pointers_attempted == 0:
            return 0
        else:
            return round((obj.three_pointers_made/obj.three_pointers_attempted) * 100, 2)

    @extend_schema_field(OpenApiTypes.FLOAT)
    def get_free_throw_percentage(self, obj):
        if obj.free_throws_attempted == 0:
            return 0
        else:
            return round((obj.free_throws_made/obj.free_throws_attempted) * 100, 2)

    def validate(self, data):
        player = data['player']
        game = data['game']
        fgm = data['field_goals_made']
        fga = data['field_goals_attempted']
        tpm = data['three_pointers_made']
        tpa = data['three_pointers_attempted']
        ftm = data['free_throws_made']
        fta = data['free_throws_attempted']

        if Stats.objects.filter(game=game, player=player).exclude(
                pk=self.instance.pk if self.instance else None
        ).exists():
            raise serializers.ValidationError('Cannot have two instances of stats of the same player in one game.')

        if player.team != game.home_team and player.team != game.away_team:
            raise serializers.ValidationError('This player is not in the team participating in the game.')

        if fgm > fga or tpm > tpa or ftm > fta:
            raise serializers.ValidationError(
                "The number of shots made can't be greater than the number of shots attempted."
            )

        if tpa > fga:
            raise serializers.ValidationError(
                "The number of three pointers attempted can't be greater than the number of field goals attempted."
            )

        if tpm > fgm:
            raise serializers.ValidationError(
                "The number of three pointers made can't be greater than the number of field goals made."
            )

        return data

    def validate_field_goals_made(self, value):
        return validate_nonnegative(value, 'The number of field goals made has to be non-negative.')

    def validate_field_goals_attempted(self, value):
        return validate_nonnegative(value, 'The number of field goals attempted has to be non-negative.')

    def validate_three_pointers_made(self, value):
        return validate_nonnegative(value, 'The number of three pointers made has to be non-negative.')

    def validate_three_pointers_attempted(self, value):
        return validate_nonnegative(value, 'The number of three pointers attempted has to be non-negative.')

    def validate_free_throws_made(self, value):
        return validate_nonnegative(value, 'The number of free throws made has to be non-negative.')

    def validate_free_throws_attempted(self, value):
        return validate_nonnegative(value, 'The number of free throws attempted has to be non-negative.')

    def validate_offensive_rebounds(self, value):
        return validate_nonnegative(value, 'The number of offensive rebounds has to be non-negative.')

    def validate_defensive_rebounds(self, value):
        return validate_nonnegative(value, 'The number of defensive rebounds has to be non-negative.')

    def validate_assists(self, value):
        return validate_nonnegative(value, 'The number of assists has to be non-negative.')

    def validate_steals(self, value):
        return validate_nonnegative(value, 'The number of steals has to be non-negative.')

    def validate_blocks(self, value):
        return validate_nonnegative(value, 'The number of blocks has to be non-negative.')

    def validate_turnovers(self, value):
        return validate_nonnegative(value, 'The number of turnovers has to be non-negative.')
