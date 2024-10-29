import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.roulette import (
    RouletteGame,
    ConservativeBot,
    AggressiveBot,
    RandomBot,
    OnlyGreenBot,
    Bet,
)


@pytest.fixture
def setup_game() -> RouletteGame:
    bots = [
        ConservativeBot(name="Arthur", budget=100),
        AggressiveBot(name="Denis", budget=100),
        RandomBot(name="Misha", budget=100),
        OnlyGreenBot(name="Mark", budget=100),
    ]
    game = RouletteGame(bots)
    return game


def test_initial_state(setup_game: RouletteGame) -> None:
    game = setup_game
    assert game.round == 1
    for bot in game.bots:
        assert bot.budget == 100


def test_spin_wheel(setup_game: RouletteGame) -> None:
    game = setup_game
    number, color = game.spin_wheel()
    assert 0 <= number < game.NUMBER_OF_FIELDS
    assert color in game.COLORS


def test_budget_update(setup_game: RouletteGame) -> None:
    game = setup_game
    bot = game.bots[0]
    initial_budget = bot.budget
    bot.update_budget(50)
    assert bot.budget == initial_budget + 50


def test_bet_evaluation_color(setup_game: RouletteGame) -> None:
    game = setup_game
    winning_number = 1
    winning_color = "Red"
    bet = Bet(amount=10, bet_type="color", choice="Red")
    result = game.evaluate_bets(bet, winning_number, winning_color)
    assert result == 20


def test_bet_evaluation_number(setup_game: RouletteGame) -> None:
    game = setup_game
    winning_number = 17
    winning_color = "Black"
    bet = Bet(amount=10, bet_type="number", choice=17)
    result = game.evaluate_bets(bet, winning_number, winning_color)
    assert result == 360


def test_bet_evaluation_green(setup_game: RouletteGame) -> None:
    game = setup_game
    winning_number = 0
    winning_color = "Green"
    bet = Bet(amount=10, bet_type="color", choice="Green")
    result = game.evaluate_bets(bet, winning_number, winning_color)
    assert result == 350


def test_play_round(setup_game: RouletteGame) -> None:
    game = setup_game
    initial_budgets = [bot.budget for bot in game.bots]
    game.play_round()
    assert game.round == 2
    assert any(bot.budget != initial_budgets[i] for i, bot in enumerate(game.bots))


def test_game_progression(setup_game: RouletteGame) -> None:
    game = setup_game
    game.play()
    assert game.round > 1
    assert game.round <= game.max_steps + 1 or all(bot.budget <= 0 for bot in game.bots)


def test_winning_condition(setup_game: RouletteGame) -> None:
    game = setup_game
    for bot in game.bots:
        bot.update_budget(1000 - bot.budget)
    winner = game.check_for_winner()
    assert winner is not None
    assert winner.budget >= game.WINNING_BUDGET
