from typing import Tuple, Dict, Union

from django.db.models import Max, Count

from jankenfw.game.enum import MoveChoices, GameStatusChoices
from jankenfw.game.models import Move, GameRound, Player, Game


def join_game(game: Game, player: Player) -> Dict:
    """
    Add a player to the provided game.

    Return an error if:
        - a player already joined a game
        - the game is full
        - the game is finished
    """

    if game.player.filter(id=player.id).exists():
        return {"error": "You have already joined this game."}
    elif game.status == GameStatusChoices.FINISHED:
        return {"error": "This game is finished."}
    elif game.player.count() >= 2:
        return {"error": "This game is full."}

    game.player.add(player)

    if game.player.count() == 2:
        game.status = GameStatusChoices.IN_PROGRESS
        game.save()

    return {"status": "You joined the game."}


def _get_current_round(game: Game) -> Tuple[int, GameRound]:
    """
    Get current round object and current round number of the provided game.
    """

    game_rounds = GameRound.objects.filter(game=game)
    current_game_round_number = game_rounds.aggregate(Max("round_number"))[
        "round_number__max"
    ]
    game_round = game_rounds.get(round_number=current_game_round_number)

    return current_game_round_number, game_round


def _findout_winner(game: Game, game_round: GameRound) -> str:
    """
    Findout who is the winner of the round or game.
    """

    moves = Move.objects.filter(game_round=game_round)
    player_one = moves[0].player
    player_one_move = moves[0].move
    player_two = moves[1].player
    player_two_move = moves[1].move

    winner = ""

    # TODO: Create better move mapping to find a winner
    if player_one_move == player_two_move:
        winner = "Tie"
    elif (
        player_one_move == MoveChoices.Rock and player_two_move == MoveChoices.Scissors
    ):
        winner = player_one
    elif player_one_move == MoveChoices.Rock and player_two_move == MoveChoices.Paper:
        winner = player_two
    elif (
        player_one_move == MoveChoices.Scissors and player_two_move == MoveChoices.Rock
    ):
        winner = player_two
    elif (
        player_one_move == MoveChoices.Scissors and player_two_move == MoveChoices.Paper
    ):
        winner = player_one
    elif player_one_move == MoveChoices.Paper and player_two_move == MoveChoices.Rock:
        winner = player_one
    elif (
        player_one_move == MoveChoices.Paper and player_two_move == MoveChoices.Scissors
    ):
        winner = player_two

    if winner != "Tie":
        game_round.winner = winner
        game_round.save()

    if game_round.round_number < game.rounds:
        if winner == "Tie":
            return f"Round finished. It's a Tie"
        return f"{game_round.round_number} round winner is {winner}"

    elif game_round.round_number == game.rounds:
        win_count = (
            GameRound.objects.filter(game=game)
            .values_list("winner")
            .annotate(winner_count=Count("winner"))
            .order_by("-winner_count")
        )
        # No winners at this game
        if win_count[0][0] is None:
            return f"The game finished. It's a Tie."

        player_one_games_won = win_count[0][1]
        player_two_games_won = win_count[1][1]

        if player_one_games_won == player_two_games_won:
            return f"The game finished. It's a Tie."

        winner_id, rounds_won = win_count[0]

        player = Player.objects.get(id=winner_id)
        player.games_won += 1
        player.save()

        game.status = GameStatusChoices.FINISHED
        game.save()

        return f"Game winner is {player}. Total rounds won {rounds_won}. Total games won {player.games_won}"


def _is_game_active(game: Game) -> Dict:
    """
    Check if the game is in progress.

    Return an error if:
        - game in finished
        - there is one player missing
    """

    if game.status == GameStatusChoices.FINISHED:
        return {"error": "This game is finished."}
    elif game.status == GameStatusChoices.WAITING_FOR_PLAYER:
        return {"error": "Waiting for players."}

    return {"status": "This game is in progress."}


def do_move(game: Game, move: Move, player: Player) -> Dict:
    """
    Create a Move object for provided Player and Game.

    If there are already two moves in the current game round, and it is not the last round
    create a new Round.

    For finished round call a 'findout_winner' method to get the round/game winner.

    Next set a player who should do next move.
    """

    other_player = game.player.exclude(id=player.id).first()
    current_game_round_number, game_round = _get_current_round(game)
    moves_in_current_round = Move.objects.filter(game_round=game_round).count()

    if moves_in_current_round >= 2 and current_game_round_number < game.rounds:
        game_round = GameRound.objects.create(
            game=game, round_number=current_game_round_number + 1
        )

    if game.next_move == player or not game.next_move:
        Move.objects.create(game=game, player=player, move=move, game_round=game_round)

        moves_in_current_round = Move.objects.filter(game_round=game_round).count()
        if moves_in_current_round >= 2:
            status = _findout_winner(game, game_round)
            game.next_move = None
            game.save()
            return {"status": status}

        game.next_move = other_player
        game.save()
