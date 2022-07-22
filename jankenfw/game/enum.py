from django.db import models


class MoveChoices(models.IntegerChoices):
    """
    All possible moves in Rock, Paper, Scissors, Lizard, Spock game
    """

    Rock = 1, "rock"
    Paper = 2, "paper"
    Scissors = 3, "scissors"
    # TODO: Implement below options
    # Lizard = 4, "lizard"
    # Spock = 5, "spock"


class GameStatusChoices(models.IntegerChoices):
    """
    Statues which represent all possible game states.
    """

    WAITING_FOR_PLAYER = 1, "waiting for player"
    IN_PROGRESS = 2, "in progress"
    FINISHED = 3, "finished"
