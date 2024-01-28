from rest_framework import serializers
from api.models import Team, Coach, Player


class CoachSerializer(serializers.HyperlinkedModelSerializer):
    current_team_name_abbreviation = serializers.SerializerMethodField()

    class Meta:
        model = Coach
        fields = ['url', 'id', 'name', 'date_of_birth', 'current_team', 'current_team_name_abbreviation']

    def get_current_team_name_abbreviation(self, obj):
        team_instance = obj.current_team
        return team_instance.name_abbreviation


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

    def get_team_name_abbreviation(self, obj):
        team_instance = obj.team
        return team_instance.name_abbreviation


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    players = serializers.SerializerMethodField()
    coach = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['url', 'id', 'name_abbreviation', 'full_name', 'coach', 'players']

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
