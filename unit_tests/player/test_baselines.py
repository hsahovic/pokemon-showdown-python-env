# -*- coding: utf-8 -*-
from poke_env.environment.move import Move
from poke_env.environment.pokemon import Pokemon
from poke_env.player.baselines import MaxBasePowerPlayer
from poke_env.player.baselines import SimpleHeuristicsPlayer
from collections import namedtuple


def test_max_base_power_player():
    player = MaxBasePowerPlayer(start_listening=False)

    PseudoBattle = namedtuple(
        "PseudoBattle",
        (
            "available_moves",
            "available_switches",
            "can_z_move",
            "can_dynamax",
            "can_mega_evolve",
        ),
    )
    battle = PseudoBattle([], [], False, False, False)

    assert player.choose_move(battle) == "/choose default"

    battle.available_switches.append(Pokemon(species="ponyta"))
    assert player.choose_move(battle) == "/choose switch ponyta"

    battle.available_moves.append(Move("protect"))
    assert player.choose_move(battle) == "/choose move protect"

    battle.available_moves.append(Move("quickattack"))
    assert player.choose_move(battle) == "/choose move quickattack"

    battle.available_moves.append(Move("flamethrower"))
    assert player.choose_move(battle) == "/choose move flamethrower"


def test_simple_heuristics_player_estimate_matchup():
    player = SimpleHeuristicsPlayer(start_listening=False)

    dragapult = Pokemon(species="dragapult")
    assert player._estimate_matchup(dragapult, dragapult) == 0

    gengar = Pokemon(species="gengar")
    assert player._estimate_matchup(dragapult, gengar) == -player._estimate_matchup(
        gengar, dragapult
    )
    assert player._estimate_matchup(dragapult, gengar) == player.SPEED_TIER_COEFICIENT

    mamoswine = Pokemon(species="mamoswine")
    assert (
        player._estimate_matchup(dragapult, mamoswine)
        == -1 + player.SPEED_TIER_COEFICIENT
    )

    dragapult._set_hp("100/100")
    mamoswine._set_hp("50/100")
    assert (
        player._estimate_matchup(dragapult, mamoswine)
        == -1 + player.SPEED_TIER_COEFICIENT + player.HP_FRACTION_COEFICIENT / 2
    )
