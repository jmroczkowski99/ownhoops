from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from api.models import Team, Coach, Player, Game
from api.validators import (
    validate_alpha_and_title,
    validate_future_date,
    validate_positive
)


class CoachSerializer(serializers.HyperlinkedModelSerializer):
    current_team_name_abbreviation = serializers.SerializerMethodField()

    class Meta:
        model = Coach
        fields = ['url', 'id', 'name', 'date_of_birth', 'current_team', 'current_team_name_abbreviation']

    def get_current_team_name_abbreviation(self, obj):
        team_instance = obj.current_team
        return team_instance.name_abbreviation

    def validate_name(self, value):
        return validate_alpha_and_title(value, 'Name should only contain letters.', 'Name should be capitalized.')

    def validate_date_of_birth(self, value):
        return validate_future_date(value, 'Birth date cannot be in the future.')


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    team_name_abbreviation = serializers.SerializerMethodField()

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
            'rebounds_per_game',
            'assists_per_game',
            'steals_per_game',
            'blocks_per_game',
            'turnovers_per_game',
            'field_goal_percentage',
            'three_point_field_goal_percentage',
            'free_throw_percentage',
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=Player.objects.all(),
                fields=['jersey_number', 'team'],
                message='This jersey number is already assigned to a player in this team.'
            )
        ]

    def get_team_name_abbreviation(self, obj):
        team_instance = obj.team
        return team_instance.name_abbreviation

    def validate_name(self, value):
        return validate_alpha_and_title(value, 'Name should only contain letters.', 'Name should be capitalized.')

    def validate_date_of_birth(self, value):
        return validate_future_date(value, 'Birth date cannot be in the future.')

    def validate_country(self, value):
        return validate_alpha_and_title(
            value,
            'Country name should only contain letters.',
            'Country name should be capitalized.'
        )

    def validate_height(self, value):
        return validate_positive(value, 'Height must be greater than 0.')

    def validate_weight(self, value):
        return validate_positive(value, 'Weight must be greater than 0.')

    def validate_jersey_number(self, value):
        if not 0 <= value <= 99:
            raise serializers.ValidationError('Invalid jersey number. Only numbers 0-99 are allowed.')
        return value


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    players = serializers.SerializerMethodField()
    coach = serializers.SerializerMethodField()
    games = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['url', 'id', 'name_abbreviation', 'full_name', 'coach', 'players', 'games']

    def get_coach(self, obj):
        coach_instance = obj.coach
        coach_data = CoachSerializer(coach_instance, context=self.context).data
        return {
            'url': coach_data.get('url', None),
            'id': coach_data.get('id', None),
            'name': coach_data.get('name', None),
        }

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

    def get_games(self, obj):
        games_queryset = obj.home_games.all() | obj.away_games.all()
        games_data = GameSerializer(games_queryset, many=True, context=self.context).data

        return [
            {
                'url': game_data.get('url', None),
                'id': game_data.get('id', None),
                'info': (
                    f"{game_data.get('away_team_name_abbreviation', None)} @ "
                    f"{game_data.get('home_team_name_abbreviation', None)} - "
                    f"{game_data.get('date', None)}",
                )
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
        if not value.istitle():
            raise serializers.ValidationError('Team name should be capitalized.')
        return value


class GameSerializer(serializers.HyperlinkedModelSerializer):
    home_team_name_abbreviation = serializers.ReadOnlyField(source='home_team.name_abbreviation')
    away_team_name_abbreviation = serializers.ReadOnlyField(source='away_team.name_abbreviation')

    class Meta:
        model = Game
        fields = [
            'url',
            'id',
            'date',
            'home_team',
            'home_team_name_abbreviation',
            'away_team',
            'away_team_name_abbreviation',
            'home_team_score',
            'away_team_score',
        ]
