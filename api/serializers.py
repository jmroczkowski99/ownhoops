from rest_framework import serializers
from api.models import Team, Coach, Player


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Team
        fields = ['url', 'id', 'name_abbreviation', 'full_name']


class CoachSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Coach
        fields = ['url', 'id', 'name', 'date_of_birth', 'current_team']


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Player
        fields = [
            'url', 'id', 'name', 'team', 'date_of_birth', 'country', 'position', 'height', 'weight',
            'points_per_game', 'rebounds_per_game', 'assists_per_game', 'steals_per_game',
            'blocks_per_game', 'turnovers_per_game', 'field_goal_percentage',
            'three_point_field_goal_percentage', 'free_throw_percentage'
        ]
