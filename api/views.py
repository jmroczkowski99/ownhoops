from api.models import Team, Coach, Player, Game, Stats
from api.serializers import TeamSerializer, CoachSerializer, PlayerSerializer, GameSerializer, StatsSerializer
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


class StatsViewSet(viewsets.ModelViewSet):
    queryset = Stats.objects.all()
    serializer_class = StatsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        game_id = self.kwargs.get('game_pk')
        player_id = self.kwargs.get('player_pk')
        if game_id:
            game_stats = Stats.objects.filter(game_id=game_id).order_by('player__team')
            return game_stats
        elif player_id:
            game_stats = Stats.objects.filter(player_id=player_id)
            return game_stats
        else:
            return Stats.objects.all()
