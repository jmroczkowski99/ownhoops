import pytest


class TestTeamModel:
    @pytest.mark.django_db
    def test_team_str_method(self, create_first_team):
        team = create_first_team
        assert str(team) == 'MIA'


class TestCoachModel:
    @pytest.mark.django_db
    def test_coach_str_method(self, create_first_coach):
        coach = create_first_coach
        assert str(coach) == 'Erik Spoelstra'


class TestPlayerModel:
    @pytest.mark.django_db
    def test_player_str_method(self, create_first_player):
        player = create_first_player
        assert str(player) == 'Jimmy Butler - DOB: 1988-01-01'


class TestGameModel:
    @pytest.mark.django_db
    def test_game_str_method(self, create_first_game):
        game = create_first_game
        assert str(game) == 'GSW @ MIA - 2024-01-01'


class TestStatsModel:
    @pytest.mark.django_db
    def test_stats_str_method(self, create_first_statline):
        stats = create_first_statline
        assert str(stats) == 'GSW @ MIA - 2024-01-01 - Jimmy Butler - DOB: 1988-01-01 stats'
