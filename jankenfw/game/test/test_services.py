from unittest import TestCase
from django.forms.models import model_to_dict
from django.contrib.auth import get_user_model

from jankenfw.game.services import join_game, _get_current_round, _is_game_active
from jankenfw.game.enum import GameStatusChoices
from jankenfw.game.test.factories import PlayerFactory, GameFactory, GameRoundFactory
from jankenfw.users.test.factories import UserFactory


class TestServices(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.player_one = PlayerFactory(user=self.user)
        self.game = GameFactory(status=GameStatusChoices.WAITING_FOR_PLAYER)
        self.game_round = GameRoundFactory(game=self.game, round_number=1)

    def test_join_game(self):
        result = join_game(self.game, self.player_one)

        self.assertEqual(result["status"], "You joined the game.")

    def test_join_game__twice(self):
        join_game(self.game, self.player_one)
        result = join_game(self.game, self.player_one)

        self.assertEqual(result["error"], "You have already joined this game.")

    def test_join_game__finished(self):
        self.game = GameFactory(status=GameStatusChoices.FINISHED)
        self.game.save()
        result = join_game(self.game, self.player_one)

        self.assertEqual(result["error"], "This game is finished.")

    def test_join_game__full(self):
        self.game.player.add(PlayerFactory(), PlayerFactory())
        self.game.save()
        result = join_game(self.game, self.player_one)

        self.assertEqual(result["error"], "This game is full.")

    def test_get_current_round(self):
        self.game.player.add(PlayerFactory(), PlayerFactory())
        self.game.save()
        result = _get_current_round(self.game)

        self.assertEqual(result, (self.game_round.round_number, self.game_round))

    def test_is_game_active(self):
        result = _is_game_active(self.game)

        self.assertEqual(result["error"], "Waiting for players.")

        self.game.status = GameStatusChoices.IN_PROGRESS
        self.game.save()
        result = _is_game_active(self.game)

        self.assertEqual(result["status"], "This game is in progress.")

        self.game.status = GameStatusChoices.FINISHED
        self.game.save()
        result = _is_game_active(self.game)

        self.assertEqual(result["error"], "This game is finished.")

    def test_do_move(self):
        # TODO
        ...

    def test_findout_winner(self):
        # TODO
        ...
