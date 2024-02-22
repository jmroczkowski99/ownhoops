import pytest
from django.urls import reverse
from rest_framework import status


class TestBasicRouter:
    @pytest.mark.django_db
    def test_team_list_url(self, api_client):
        response = api_client.get(reverse('team-list'))
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_team_detail_url(self, api_client, create_first_team):
        response = api_client.get(reverse('team-detail', args=[create_first_team.id]))
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_coaches_list_url(self, api_client):
        response = api_client.get(reverse('coach-list'))
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_coach_detail_url(self, api_client, create_first_coach):
        response = api_client.get(reverse('coach-detail', args=[create_first_coach.id]))
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_players_list_url(self, api_client):
        response = api_client.get(reverse('player-list'))
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_player_detail_url(self, api_client, create_first_player):
        response = api_client.get(reverse('player-detail', args=[create_first_player.id]))
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_games_list_url(self, api_client):
        response = api_client.get(reverse('game-list'))
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_game_detail_url(self, api_client, create_first_game):
        response = api_client.get(reverse('game-detail', args=[create_first_game.id]))
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_stats_list_url(self, api_client):
        response = api_client.get(reverse('stats-list'))
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_stats_detail_url(self, api_client, create_first_statline):
        response = api_client.get(reverse('stats-detail', args=[create_first_statline.id]))
        assert response.status_code == status.HTTP_200_OK


class TestTeamRouter:
    @pytest.mark.django_db
    def test_team_coach_list_url(self, api_client, create_first_team):
        team_url = reverse("team-detail", args=[create_first_team.id])
        team_coach_list_url = f"{team_url}coach/"
        response = api_client.get(team_coach_list_url)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_team_coach_detail_url(self, api_client, create_first_team, create_first_coach):
        team_url = reverse("team-detail", args=[create_first_team.id])
        team_coach_url = f"{team_url}coach/{create_first_coach.id}/"
        response = api_client.get(team_coach_url)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_team_players_list_url(self, api_client, create_first_team):
        team_url = reverse("team-detail", args=[create_first_team.id])
        team_players_list_url = f"{team_url}players/"
        response = api_client.get(team_players_list_url)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_team_player_detail_url(self, api_client, create_first_team, create_first_player):
        team_url = reverse("team-detail", args=[create_first_team.id])
        team_player_url = f"{team_url}players/{create_first_player.id}/"
        response = api_client.get(team_player_url)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_team_games_list_url(self, api_client, create_first_team):
        team_url = reverse("team-detail", args=[create_first_team.id])
        team_games_list_url = f"{team_url}games/"
        response = api_client.get(team_games_list_url)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_team_game_detail_url(self, api_client, create_first_team, create_first_game):
        team_url = reverse("team-detail", args=[create_first_team.id])
        team_game_url = f"{team_url}games/{create_first_game.id}/"
        response = api_client.get(team_game_url)
        assert response.status_code == status.HTTP_200_OK


class TestGamesRouter:
    @pytest.mark.django_db
    def test_game_stats_list_url(self, api_client, create_first_game):
        game_url = reverse("game-detail", args=[create_first_game.id])
        game_stats_list_url = f"{game_url}stats/"
        response = api_client.get(game_stats_list_url)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_game_stats_detail_url(self, api_client, create_first_game, create_first_statline):
        game_url = reverse("game-detail", args=[create_first_game.id])
        game_stats_url = f"{game_url}stats/{create_first_statline.id}/"
        response = api_client.get(game_stats_url)
        assert response.status_code == status.HTTP_200_OK


class TestPlayerRouter:
    @pytest.mark.django_db
    def test_player_stats_list_url(self, api_client, create_first_player):
        player_url = reverse("player-detail", args=[create_first_player.id])
        player_stats_list_url = f"{player_url}stats/"
        response = api_client.get(player_stats_list_url)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_player_stats_detail_url(self, api_client, create_first_player, create_first_statline):
        player_url = reverse("player-detail", args=[create_first_player.id])
        player_stats_url = f"{player_url}stats/{create_first_statline.id}/"
        response = api_client.get(player_stats_url)
        assert response.status_code == status.HTTP_200_OK
