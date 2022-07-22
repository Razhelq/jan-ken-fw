from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from jankenfw.game.enum import GameStatusChoices
from jankenfw.game.test.factories import PlayerFactory, GameRoundFactory, GameFactory
from jankenfw.game.models import Game, Move
from jankenfw.users.test.factories import UserFactory

fake = Faker()


class GameViewSetTestCase(APITestCase):
    """
    Tests GameViewSet
    """

    def setUp(self):
        self.user = UserFactory()
        self.player_one = PlayerFactory(user=self.user)
        self.player_two = PlayerFactory(user=UserFactory())
        self.player_three = PlayerFactory(user=UserFactory())
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user.auth_token}")
        self.game = GameFactory(status=GameStatusChoices.WAITING_FOR_PLAYER)

    def test_join_game(self):
        url = reverse("game-join", kwargs={"pk": self.game.id})
        response = self.client.post(url, {})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_join_game__twice(self):
        url = reverse("game-join", kwargs={"pk": self.game.id})
        self.client.post(url, {})
        response = self.client.post(url, {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data.get("error"), "You have already joined this game."
        )

    def test_join_game__full(self):
        self.game.player.add(self.player_two, self.player_three)
        self.game.save()
        url = reverse("game-join", kwargs={"pk": self.game.id})
        response = self.client.post(url, {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("error"), "This game is full.")

    def test_join_game__finished(self):
        self.game.status = GameStatusChoices.FINISHED
        self.game.save()
        url = reverse("game-join", kwargs={"pk": self.game.id})
        response = self.client.post(url, {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("error"), "This game is finished.")

    def _set_up_game(self):
        self.game_round = GameRoundFactory(game=self.game, round_number=1)
        self.game.player.add(self.player_one, self.player_two)
        self.game.status = GameStatusChoices.IN_PROGRESS
        self.game.next_move = None
        self.game.save()

    def test_move(self):
        self._set_up_game()
        url = reverse("game-move", kwargs={"pk": self.game.id})
        response = self.client.post(url, {"move": 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Move.objects.filter(game=self.game).exists())

    def test_move__not_player_move(self):
        self._set_up_game()
        self.game.next_move = self.player_two
        self.game.save()
        url = reverse("game-move", kwargs={"pk": self.game.id})
        response = self.client.post(url, {"move": 1})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("error"), "It's not your move.")

    def test_move__wrong_move(self):
        self._set_up_game()
        url = reverse("game-move", kwargs={"pk": self.game.id})
        response = self.client.post(url, {"move": 7})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(url, {"move": "123213"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class HighScoreAPITestCase(APITestCase):
    """
    Tests HighScoreAPI
    """

    def setUp(self):
        self.user = UserFactory()
        self.player_one = PlayerFactory(user=self.user, games_won=3)
        self.player_two = PlayerFactory(user=UserFactory(), games_won=33)
        self.player_three = PlayerFactory(user=UserFactory(), games_won=333)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user.auth_token}")
        self.game = Game.objects.create()

    def test_high_score(self):
        url = reverse("player-list")
        response = self.client.get(url, {})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.player_three.user.username, response.data["results"][0]["username"]
        )
        self.assertEqual(
            self.player_three.games_won, response.data["results"][0]["games_won"]
        )
        self.assertEqual(
            self.player_two.user.username, response.data["results"][1]["username"]
        )
        self.assertEqual(
            self.player_two.games_won, response.data["results"][1]["games_won"]
        )
        self.assertEqual(
            self.player_one.user.username, response.data["results"][2]["username"]
        )
        self.assertEqual(
            self.player_one.games_won, response.data["results"][2]["games_won"]
        )
