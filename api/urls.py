from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from api import views

router = DefaultRouter()
router.register(r'teams', views.TeamViewSet, basename='team')
router.register(r'coaches', views.CoachViewSet, basename='coach')
router.register(r'players', views.PlayerViewSet, basename='player')
router.register(r'games', views.GameViewSet, basename='game')

teams_router = routers.NestedSimpleRouter(router, r'teams', lookup='team')
teams_router.register(r'coach', views.CoachViewSet, basename='team-coach')
teams_router.register(r'players', views.PlayerViewSet, basename='team-player')
teams_router.register(r'games', views.GameViewSet, basename='team-game')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(teams_router.urls)),
]
