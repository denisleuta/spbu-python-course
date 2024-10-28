import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.roulette import (
    RouletteGame,
    ConservativeBot,
    AggressiveBot,
    RandomBot,
    Bet,
)


@pytest.fixture
def setup_game() -> RouletteGame:
    bots = [
        ConservativeBot(name="ConservativeBot", budget=100),
        AggressiveBot(name="AggressiveBot", budget=100),
        RandomBot(name="RandomBot", budget=100),
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
    assert 0 <= number <= 36
    assert color in game.COLORS


def test_budget_update(setup_game: RouletteGame) -> None:
    game = setup_game
    bot = game.bots[0]
    initial_budget = bot.budget
    bot.update_budget(50)
    assert bot.budget == initial_budget + 50


def test_bet_evaluation(setup_game: RouletteGame) -> None:
    game = setup_game
    winning_number = 5
    winning_color = "Red"
    bet = Bet(amount=10, bet_type="color", choice="Red")
    result = game.evaluate_bets(bet, winning_number, winning_color)
    assert result == 20  # Color match doubles the bet amount


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
    assert game.round <= game.MAX_STEPS + 1 or all(bot.budget <= 0 for bot in game.bots)
