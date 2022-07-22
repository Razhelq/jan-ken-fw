from django.contrib.auth import get_user_model

from django.db import models

from libs.models import BaseModel
from jankenfw.game.enum import GameStatusChoices, MoveChoices


class Player(BaseModel):
    """
    The relationship that places a player in a game.
    """

    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    games_won = models.IntegerField(default=0, help_text="Total number of won games.")

    def __str__(self):
        return str(self.user.username)


class Game(BaseModel):
    """
    A Game object represents a single game.
    """

    player = models.ManyToManyField(Player, blank=True)
    rounds = models.SmallIntegerField(default=1, help_text="Number of rounds")
    status = models.SmallIntegerField(
        choices=GameStatusChoices.choices,
        default=GameStatusChoices.WAITING_FOR_PLAYER,
        help_text="Status that represents a game state.",
    )
    next_move = models.ForeignKey(
        Player,
        on_delete=models.DO_NOTHING,
        related_name="next_move",
        null=True,
        help_text="A player who should do next move.",
    )


class GameRound(BaseModel):
    """
    The relationship that connects a round with game and stores round winner.
    """

    winner = models.ForeignKey(
        Player,
        on_delete=models.DO_NOTHING,
        related_name="winner",
        null=True,
        help_text="A winner of the round.",
    )
    round_number = models.SmallIntegerField(default=1)
    game = models.ForeignKey(
        Game, on_delete=models.DO_NOTHING, related_name="game_round", null=True
    )


class Move(BaseModel):
    """
    The relationship that connects a move with game, player and round.
    """

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    move = models.SmallIntegerField(choices=MoveChoices.choices, null=True)
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING, null=True)
    game_round = models.ForeignKey(GameRound, on_delete=models.DO_NOTHING, null=True)
