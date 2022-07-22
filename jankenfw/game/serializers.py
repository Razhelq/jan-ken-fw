from rest_framework import serializers

from jankenfw.game.models import Game, Move, GameRound, Player


class GameSerializer(serializers.ModelSerializer):
    """
    Serialize a Game object
    """

    class Meta:
        model = Game
        fields = "__all__"
        read_only_fields = ("player", "status", "next_move")


class MoveSerializer(serializers.ModelSerializer):
    """
    Serialize a Move object
    """

    class Meta:
        model = Move
        fields = "__all__"
        read_only_fields = ("game",)


class GameRoundSerializer(serializers.ModelSerializer):
    """
    Serialize a GameRound object
    """

    class Meta:
        model = GameRound
        fields = "__all__"


class PlayerHighScoreSerializer(serializers.ModelSerializer):
    """
    Serialize a Player object to provide a high score list of the best players
    """

    username = serializers.CharField(source="user.username")

    class Meta:
        model = Player
        fields = (
            "username",
            "games_won",
        )
        read_only_fields = fields
