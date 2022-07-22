from uuid import UUID

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from jankenfw.game.models import Game, Player, GameRound
from jankenfw.game.serializers import (
    GameSerializer,
    MoveSerializer,
    PlayerHighScoreSerializer,
)
from jankenfw.game.services import join_game, _is_game_active, do_move


class GameViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer: GameSerializer) -> None:
        """
        Create Game object and related first game round.
        """

        game = serializer.save()
        GameRound.objects.create(game=game)

    @action(detail=True, methods=["post"])
    def join(self, request, pk: UUID) -> Response:
        """
        Create a player object for the provided game and call 'join_game' function
        to add a player to the game.

        Return 400 if 'join_game' function returns any error.
        """

        game = self.get_object()
        player, _ = Player.objects.get_or_create(user=request.user)

        result = join_game(game, player)

        if "error" in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        sz = self.get_serializer(game)

        return Response(sz.data)

    @action(detail=True, methods=["post"], serializer_class=MoveSerializer)
    def move(self, request, pk: UUID) -> Response:
        """
        For active game nad valid move call 'do_move' function to create a Move object.

        Return 400 for in case of invalid move.
        """

        game = self.get_object()

        result = _is_game_active(game)
        if "error" in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        player = Player.objects.get(user=request.user)
        if game.next_move and game.next_move != player:
            return Response(
                {"error": "It's not your move."}, status=status.HTTP_400_BAD_REQUEST
            )

        sz = self.get_serializer(data=request.data)
        if not sz.is_valid():
            return Response(sz.errors, status=status.HTTP_400_BAD_REQUEST)

        move = sz.validated_data["move"]

        result = do_move(game=game, move=move, player=player)
        if result:
            return Response(result)
        return Response(sz.validated_data)


class HighScoreAPI(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API for providing a high score list of all players ordered by games_won value.
    """

    queryset = Player.objects.order_by("-games_won")
    serializer_class = PlayerHighScoreSerializer
    permission_classes = (AllowAny,)
