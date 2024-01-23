from api.models import Team, Coach, Player
from api.serializers import TeamSerializer, CoachSerializer, PlayerSerializer
from rest_framework import viewsets


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class CoachViewSet(viewsets.ModelViewSet):
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer

    def get_queryset(self):
        team_id = self.kwargs.get('team_pk')
        if team_id:
            return Coach.objects.filter(current_team_id=team_id)
        else:
            return Coach.objects.all()


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    def get_queryset(self):
        team_id = self.kwargs.get('team_pk')
        if team_id:
            return Player.objects.filter(team_id=team_id)
        else:
            return Player.objects.all()
