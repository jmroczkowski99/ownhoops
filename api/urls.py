from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from api import views

router = DefaultRouter()
router.register(r'teams', views.TeamViewSet, basename='team')
router.register(r'coaches', views.CoachViewSet, basename='coach')
router.register(r'players', views.PlayerViewSet, basename='player')
router.register(r'games', views.GameViewSet, basename='game')
router.register(r'stats', views.StatsViewSet, basename='stats')

teams_router = routers.NestedSimpleRouter(router, r'teams', lookup='team')
teams_router.register(r'coach', views.CoachViewSet, basename='team-coach')
teams_router.register(r'players', views.PlayerViewSet, basename='team-player')
teams_router.register(r'games', views.GameViewSet, basename='team-game')

games_router = routers.NestedSimpleRouter(router, r'games', lookup='game')
games_router.register(r'stats', views.StatsViewSet, basename='game-stats')

players_router = routers.NestedSimpleRouter(router, r'players', lookup='player')
players_router.register(r'stats', views.StatsViewSet, basename='player-stats')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(teams_router.urls)),
    path('', include(games_router.urls)),
    path('', include(players_router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
]
