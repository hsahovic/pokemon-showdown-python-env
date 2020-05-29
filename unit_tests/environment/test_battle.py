# -*- coding: utf-8 -*-
import pytest

from unittest.mock import MagicMock

from poke_env.environment.battle import Battle
from poke_env.environment.field import Field
from poke_env.environment.pokemon_type import PokemonType
from poke_env.environment.side_condition import SideCondition
from poke_env.environment.weather import Weather


def test_battle_get_pokemon():
    logger = MagicMock()
    battle = Battle("tag", "username", logger)

    #  identifier: str, force_self_team: bool = False, details: str = ""

    battle.get_pokemon("p2: azumarill", force_self_team=True)
    assert "p2: azumarill" in battle.team

    battle._player_role = "p2"

    battle._parse_message(["", "teamsize", "p1", 6])
    battle._parse_message(["", "teamsize", "p2", 6])

    battle.get_pokemon("p2a: tapukoko")
    assert "p2: tapukoko" in battle.team

    battle.get_pokemon("p1: hydreigon", details="Hydreigon, F")
    assert "p1: hydreigon" in battle.opponent_team

    assert battle.get_pokemon("p2: tapufini").species == "tapufini"
    assert battle.get_pokemon("p2: tapubulu").types == (
        PokemonType.GRASS,
        PokemonType.FAIRY,
    )
    assert battle.get_pokemon("p2: tapulele").base_stats == {
        "atk": 85,
        "def": 75,
        "hp": 70,
        "spa": 130,
        "spd": 115,
        "spe": 95,
    }
    battle.get_pokemon("p2: yveltal")

    assert len(battle.team) == 6

    with pytest.raises(ValueError):
        battle.get_pokemon("p2: pikachu")

    assert "p2: pikachu" not in battle.team


def test_battle_side_start_end():
    logger = MagicMock()
    battle = Battle("tag", "username", logger)
    battle._player_role = "p1"

    assert not battle.side_conditions

    condition = "safeguard"
    battle._side_start("p1", condition)
    battle._side_start("p2", condition)
    assert battle.side_conditions == {SideCondition.SAFEGUARD}
    assert battle.opponent_side_conditions == {SideCondition.SAFEGUARD}

    battle._side_end("p1", condition)
    battle._side_end("p2", condition)
    assert not battle.side_conditions
    assert not battle.opponent_side_conditions

    with pytest.raises(Exception):
        battle._side_end("p1", condition)

    with pytest.raises(Exception):
        battle._side_end("p2", condition)


def test_battle_field_interactions():
    logger = MagicMock()
    battle = Battle("tag", "username", logger)

    assert not battle.fields

    battle._parse_message(["", "-fieldstart", "Electric terrain"])
    assert battle.fields == {Field.ELECTRIC_TERRAIN}

    battle._parse_message(["", "-fieldstart", "Trick room"])
    assert battle.fields == {Field.ELECTRIC_TERRAIN, Field.TRICK_ROOM}

    battle._parse_message(["", "-fieldend", "Trick room"])
    assert battle.fields == {Field.ELECTRIC_TERRAIN}

    battle._parse_message(["", "-fieldend", "Electric terrain"])
    assert not battle.fields

    with pytest.raises(Exception):
        battle._parse_message(["", "-fieldend", "Electric terrain"])

    with pytest.raises(Exception):
        battle._parse_message(["", "-fieldend", "non existent field"])


def test_battle_weather_interactions():
    logger = MagicMock()
    battle = Battle("tag", "username", logger)

    assert battle.weather is None

    battle._parse_message(["", "-weather", "desolateland"])
    assert battle.weather == Weather.DESOLATELAND

    battle._parse_message(["", "-weather", "hail"])
    assert battle.weather == Weather.HAIL

    battle._parse_message(["", "-weather", "none"])
    assert battle.weather is None
