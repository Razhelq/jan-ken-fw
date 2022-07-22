from django.test import TestCase
from nose.tools import ok_

from jankenfw.game.serializers import (
    GameSerializer,
    MoveSerializer,
    GameRoundSerializer,
)
from jankenfw.game.test.factories import GameFactory, MoveFactory, GameRoundFactory


class TestGameSerializer(TestCase):
    def setUp(self):
        self.game = GameFactory()

    def test_to_representation(self):
        serializer = GameSerializer(instance=self.game, data={})
        ok_(serializer.is_valid())

        self.assertIn("id", serializer.data)
        self.assertIn("created_at", serializer.data)
        self.assertIn("updated_at", serializer.data)
        self.assertIn("rounds", serializer.data)
        self.assertIn("status", serializer.data)
        self.assertIn("next_move", serializer.data)
        self.assertIn("player", serializer.data)


class TestMoveSerializer(TestCase):
    def setUp(self):
        self.move = MoveFactory()

    def test_to_representation(self):
        serializer = MoveSerializer(instance=self.move, data={})
        ok_(serializer.is_valid())

        self.assertIn("game", serializer.data)
        self.assertIn("move", serializer.data)
        self.assertIn("player", serializer.data)
        self.assertIn("game_round", serializer.data)


class TestGameRoundSerializer(TestCase):
    def setUp(self):
        self.game_round = GameRoundFactory()

    def test_to_representation(self):
        serializer = GameRoundSerializer(instance=self.game_round, data={})
        ok_(serializer.is_valid())

        self.assertIn("winner", serializer.data)
        self.assertIn("round_number", serializer.data)
        self.assertIn("game", serializer.data)
