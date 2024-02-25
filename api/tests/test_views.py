import pytest
from django.urls import reverse
from rest_framework import status
from api.models import Player


class TestTeamViewSet:
    @pytest.mark.django_db
    def test_list_teams(self, api_client, create_first_team, create_second_team):
        response = api_client.get(reverse('team-list'))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    @pytest.mark.django_db
    def test_retrieve_team(self, api_client, create_first_team):
        response = api_client.get(reverse('team-detail', args=[create_first_team.id]))
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_create_team_unauthenticated(self, api_client):
        data = {'name_abbreviation': 'ABC', 'full_name': 'Abcers'}
        response = api_client.post(reverse('team-list'), data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_create_team_authenticated(self, api_client, create_superuser):
        api_client.force_authenticate(user=create_superuser)
        data = {'name_abbreviation': 'ABC', 'full_name': 'Abcers'}
        response = api_client.post(reverse('team-list'), data)
        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.django_db
    def test_edit_team_unauthenticated(self, api_client, create_first_team):
        data = {'name_abbreviation': 'ABC', 'full_name': 'Abcers'}
        response = api_client.put(reverse('team-detail', args=[create_first_team.id]), data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_edit_team_authenticated(self, api_client, create_superuser, create_first_team):
        api_client.force_authenticate(user=create_superuser)
        data = {'name_abbreviation': 'ABC', 'full_name': 'Abcers'}
        response = api_client.put(reverse('team-detail', args=[create_first_team.id]), data)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_delete_team_unauthenticated(self, api_client, create_first_team):
        response = api_client.delete(reverse('team-detail', args=[create_first_team.id]))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_delete_team_authenticated(self, api_client, create_superuser, create_first_team):
        api_client.force_authenticate(user=create_superuser)
        response = api_client.delete(reverse('team-detail', args=[create_first_team.id]))
        assert response.status_code == status.HTTP_204_NO_CONTENT


class TestCoachViewSet:
    @pytest.mark.django_db
    def test_list_coaches(self, api_client, create_first_coach, create_second_coach):
        response = api_client.get(reverse('coach-list'))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    @pytest.mark.django_db
    def test_list_coaches_specific_team(self, api_client, create_first_team, create_first_coach, create_second_coach):
        team_url = reverse('team-detail', args=[create_first_team.id])
        team_coach_url = f'{team_url}coach/'
        response = api_client.get(team_coach_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    @pytest.mark.django_db
    def test_retrieve_coach(self, api_client, create_first_coach):
        response = api_client.get(reverse('coach-detail', args=[create_first_coach.id]))
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_create_coach_unauthenticated(self, api_client):
        data = {'name': 'Zbigniew Boniek', 'date_of_birth': '1960-01-01'}
        response = api_client.post(reverse('coach-list'), data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_create_coach_authenticated(self, api_client, create_superuser):
        api_client.force_authenticate(user=create_superuser)
        data = {'name': 'Zbigniew Boniek', 'date_of_birth': '1960-01-01'}
        response = api_client.post(reverse('coach-list'), data)
        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.django_db
    def test_edit_coach_unauthenticated(self, api_client, create_first_coach):
        data = {'name': 'Zbigniew Boniek', 'date_of_birth': '1960-01-01'}
        response = api_client.put(reverse('coach-detail', args=[create_first_coach.id]), data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_edit_coach_authenticated(self, api_client, create_superuser, create_first_coach):
        api_client.force_authenticate(user=create_superuser)
        data = {'name': 'Zbigniew Boniek', 'date_of_birth': '1960-01-01'}
        response = api_client.put(reverse('coach-detail', args=[create_first_coach.id]), data)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_delete_coach_unauthenticated(self, api_client, create_first_coach):
        response = api_client.delete(reverse('coach-detail', args=[create_first_coach.id]))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_delete_coach_authenticated(self, api_client, create_superuser, create_first_coach):
        api_client.force_authenticate(user=create_superuser)
        response = api_client.delete(reverse('coach-detail', args=[create_first_coach.id]))
        assert response.status_code == status.HTTP_204_NO_CONTENT


class TestPlayerViewSet:
    @pytest.mark.django_db
    def test_list_players(self, api_client, create_first_player, create_second_player):
        response = api_client.get(reverse('player-list'))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    @pytest.mark.django_db
    def test_list_players_specific_team(self, api_client, create_first_team, create_first_player, create_second_player):
        team_url = reverse('team-detail', args=[create_first_team.id])
        team_players_url = f'{team_url}players/'
        response = api_client.get(team_players_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    @pytest.mark.django_db
    def test_retrieve_player(self, api_client, create_first_player):
        response = api_client.get(reverse('player-detail', args=[create_first_player.id]))
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_create_player_unauthenticated(self, api_client, create_first_team):
        data = {
            'name': 'Bam Adebayo',
            'team': create_first_team.id,
            'date_of_birth': '1997-01-01',
            'country': 'USA',
            'position': 'C',
            'height': 208,
            'weight': 110,
            'jersey_number': 13,
        }
        response = api_client.post(reverse('player-list'), data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_create_player_authenticated(self, api_client, create_first_team, create_superuser):
        api_client.force_authenticate(user=create_superuser)
        data = {
            'name': 'Bam Adebayo',
            'team': reverse('team-detail', args=[create_first_team.id]),
            'date_of_birth': '1997-01-01',
            'country': 'USA',
            'position': 'C',
            'height': 208,
            'weight': 110,
            'jersey_number': 13,
        }
        response = api_client.post(reverse('player-list'), data)
        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.django_db
    def test_edit_player_unauthenticated(self, api_client, create_first_team, create_first_player):
        data = {
            'name': 'Bam Adebayo',
            'team': reverse('team-detail', args=[create_first_team.id]),
            'date_of_birth': '1997-01-01',
            'country': 'USA',
            'position': 'C',
            'height': 208,
            'weight': 110,
            'jersey_number': 13,
        }
        response = api_client.put(reverse('player-detail', args=[create_first_player.id]), data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_edit_player_authenticated(self, api_client, create_first_team, create_superuser, create_first_player):
        api_client.force_authenticate(user=create_superuser)
        data = {
            'name': 'Bam Adebayo',
            'team': reverse('team-detail', args=[create_first_team.id]),
            'date_of_birth': '1997-01-01',
            'country': 'USA',
            'position': 'C',
            'height': 208,
            'weight': 110,
            'jersey_number': 13,
        }
        response = api_client.put(reverse('player-detail', args=[create_first_player.id]), data)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_delete_player_unauthenticated(self, api_client, create_first_player):
        response = api_client.delete(reverse('player-detail', args=[create_first_player.id]))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_delete_player_authenticated(self, api_client, create_superuser, create_first_player):
        api_client.force_authenticate(user=create_superuser)
        response = api_client.delete(reverse('player-detail', args=[create_first_player.id]))
        assert response.status_code == status.HTTP_204_NO_CONTENT


class TestGameViewSet:
    @pytest.mark.django_db
    def test_list_games(self, api_client, create_first_game, create_second_game):
        response = api_client.get(reverse('game-list'))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    @pytest.mark.django_db
    def test_list_games_specific_team(self, api_client, create_second_team, create_first_game, create_second_game):
        team_url = reverse('team-detail', args=[create_second_team.id])
        team_games_url = f'{team_url}games/'
        response = api_client.get(team_games_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    @pytest.mark.django_db
    def test_retrieve_game(self, api_client, create_first_game):
        response = api_client.get(reverse('game-detail', args=[create_first_game.id]))
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_create_game_unauthenticated(self, api_client, create_first_team, create_second_team):
        data = {
            'date': '2024-02-17',
            'home_team': reverse('team-detail', args=[create_first_team.id]),
            'away_team': reverse('team-detail', args=[create_second_team.id]),
        }
        response = api_client.post(reverse('game-list'), data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_create_game_authenticated(self, api_client, create_first_team, create_second_team, create_superuser):
        api_client.force_authenticate(user=create_superuser)
        data = {
            'date': '2024-02-17',
            'home_team': reverse('team-detail', args=[create_first_team.id]),
            'away_team': reverse('team-detail', args=[create_second_team.id]),
        }
        response = api_client.post(reverse('game-list'), data)
        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.django_db
    def test_edit_game_unauthenticated(self, api_client, create_first_game, create_first_team, create_second_team):
        data = {
            'date': '2024-02-17',
            'home_team': reverse('team-detail', args=[create_first_team.id]),
            'away_team': reverse('team-detail', args=[create_second_team.id]),
        }
        response = api_client.put(reverse('game-detail', args=[create_first_game.id]), data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_edit_game_authenticated(
            self,
            api_client,
            create_first_team,
            create_second_team,
            create_first_game,
            create_superuser
    ):
        api_client.force_authenticate(user=create_superuser)
        data = {
            'date': '2024-02-17',
            'home_team': reverse('team-detail', args=[create_first_team.id]),
            'away_team': reverse('team-detail', args=[create_second_team.id]),
        }
        response = api_client.put(reverse('game-detail', args=[create_first_game.id]), data)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_delete_game_unauthenticated(self, api_client, create_first_game):
        response = api_client.delete(reverse('game-detail', args=[create_first_game.id]))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_delete_game_authenticated(self, api_client, create_superuser, create_first_game):
        api_client.force_authenticate(user=create_superuser)
        response = api_client.delete(reverse('game-detail', args=[create_first_game.id]))
        assert response.status_code == status.HTTP_204_NO_CONTENT


class TestStatsViewSet:
    @pytest.mark.django_db
    def test_list_stats(self, api_client, create_first_statline, create_second_statline, create_third_statline):
        response = api_client.get(reverse('stats-list'))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    @pytest.mark.django_db
    def test_list_stats_specific_game(
            self,
            api_client,
            create_first_game,
            create_first_statline,
            create_second_statline,
            create_third_statline,
            create_first_team
    ):
        game_url = reverse('game-detail', args=[create_first_game.id])
        game_stats_url = f'{game_url}stats/'
        response = api_client.get(game_stats_url)
        first_listed_player_id = int(response.data[0]['player'].split('/')[-2])
        player_instance = Player.objects.get(pk=first_listed_player_id)
        player_instance_team = reverse('team-detail', args=[player_instance.team.id])
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert player_instance_team == reverse('team-detail', args=[create_first_team.id])

    @pytest.mark.django_db
    def test_list_stats_specific_player(
            self,
            api_client,
            create_first_player,
            create_first_statline,
            create_second_statline,
            create_third_statline
    ):
        player_url = reverse('player-detail', args=[create_first_player.id])
        player_stats_url = f'{player_url}stats/'
        response = api_client.get(player_stats_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    @pytest.mark.django_db
    def test_retrieve_stats(self, api_client, create_first_statline):
        response = api_client.get(reverse('stats-detail', args=[create_first_statline.id]))
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_create_stats_unauthenticated(self, api_client, create_first_game, create_first_player):
        data = {
            'game': reverse('game-detail', args=[create_first_game.id]),
            'player': reverse('player-detail', args=[create_first_player.id]),
            'field_goals_made': 1,
            'field_goals_attempted': 1,
            'three_pointers_made': 1,
            'three_pointers_attempted': 1,
            'free_throws_made': 1,
            'free_throws_attempted': 1,
            'defensive_rebounds': 1,
            'offensive_rebounds': 1,
            'assists': 1,
            'steals': 1,
            'blocks': 1,
            'turnovers': 1,
        }
        response = api_client.post(reverse('stats-list'), data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_create_stats_authenticated(self, api_client, create_first_game, create_first_player, create_superuser):
        api_client.force_authenticate(user=create_superuser)
        data = {
            'game': reverse('game-detail', args=[create_first_game.id]),
            'player': reverse('player-detail', args=[create_first_player.id]),
            'field_goals_made': 1,
            'field_goals_attempted': 1,
            'three_pointers_made': 1,
            'three_pointers_attempted': 1,
            'free_throws_made': 1,
            'free_throws_attempted': 1,
            'defensive_rebounds': 1,
            'offensive_rebounds': 1,
            'assists': 1,
            'steals': 1,
            'blocks': 1,
            'turnovers': 1,
        }
        response = api_client.post(reverse('stats-list'), data)
        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.django_db
    def test_edit_stats_unauthenticated(
            self,
            api_client,
            create_first_game,
            create_first_player,
            create_first_statline
    ):
        data = {
            'game': reverse('game-detail', args=[create_first_game.id]),
            'player': reverse('player-detail', args=[create_first_player.id]),
            'field_goals_made': 1,
            'field_goals_attempted': 1,
            'three_pointers_made': 1,
            'three_pointers_attempted': 1,
            'free_throws_made': 1,
            'free_throws_attempted': 1,
            'defensive_rebounds': 1,
            'offensive_rebounds': 1,
            'assists': 1,
            'steals': 1,
            'blocks': 1,
            'turnovers': 1,
        }
        response = api_client.put(reverse('stats-detail', args=[create_first_statline.id]), data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_edit_stats_authenticated(
            self,
            api_client,
            create_first_game,
            create_first_player,
            create_first_statline,
            create_superuser
    ):
        api_client.force_authenticate(user=create_superuser)
        data = {
            'game': reverse('game-detail', args=[create_first_game.id]),
            'player': reverse('player-detail', args=[create_first_player.id]),
            'field_goals_made': 1,
            'field_goals_attempted': 1,
            'three_pointers_made': 1,
            'three_pointers_attempted': 1,
            'free_throws_made': 1,
            'free_throws_attempted': 1,
            'defensive_rebounds': 1,
            'offensive_rebounds': 1,
            'assists': 1,
            'steals': 1,
            'blocks': 1,
            'turnovers': 1,
        }
        response = api_client.put(reverse('stats-detail', args=[create_first_statline.id]), data)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_delete_stats_unauthenticated(self, api_client, create_first_statline):
        response = api_client.delete(reverse('stats-detail', args=[create_first_statline.id]))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_delete_stats_authenticated(self, api_client, create_superuser, create_first_statline):
        api_client.force_authenticate(user=create_superuser)
        response = api_client.delete(reverse('stats-detail', args=[create_first_statline.id]))
        assert response.status_code == status.HTTP_204_NO_CONTENT
