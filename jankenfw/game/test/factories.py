from factory.django import DjangoModelFactory
import factory

from jankenfw.game.enum import GameStatusChoices, MoveChoices
from jankenfw.game.models import Game, Player, GameRound, Move
from jankenfw.users.test.factories import UserFactory


class PlayerFactory(DjangoModelFactory):
    class Meta:
        model = Player

    user = factory.SubFactory(UserFactory)


class GameFactory(DjangoModelFactory):
    class Meta:
        model = Game

    status = factory.Iterator(GameStatusChoices.values)
    next_move = factory.SubFactory(PlayerFactory)


class GameRoundFactory(DjangoModelFactory):
    class Meta:
        model = GameRound

    game = factory.SubFactory(GameFactory)


class MoveFactory(DjangoModelFactory):
    class Meta:
        model = Move

    game = factory.SubFactory(GameFactory)
    move = factory.Iterator(MoveChoices.values)
    player = factory.SubFactory(PlayerFactory)
    game_round = factory.SubFactory(GameRoundFactory)
