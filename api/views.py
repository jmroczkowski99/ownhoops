from api.models import Team, Coach, Player, Game
from api.serializers import TeamSerializer, CoachSerializer, PlayerSerializer, GameSerializer
from rest_framework import viewsets
from rest_framework import permissions


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CoachViewSet(viewsets.ModelViewSet):
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        team_id = self.kwargs.get('team_pk')
        if team_id:
            return Coach.objects.filter(team_id=team_id)
        else:
            return Coach.objects.all()


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        team_id = self.kwargs.get('team_pk')
        if team_id:
            return Player.objects.filter(team_id=team_id)
        else:
            return Player.objects.all()


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        team_id = self.kwargs.get('team_pk')
        if team_id:
            team_games = Game.objects.filter(away_team_id=team_id) | Game.objects.filter(home_team_id=team_id)
            return team_games
        else:
            return Game.objects.all()
