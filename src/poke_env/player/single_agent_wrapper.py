from typing import Any, Awaitable, Dict, Optional, Tuple

from gymnasium import Env

from poke_env.player.gymnasium_api import ActionType, ObsType, PokeEnv
from poke_env.player.player import Player


class SingleAgentWrapper(Env[ObsType, ActionType]):
    def __init__(self, env: PokeEnv[ObsType, ActionType], opponent: Player):
        self.env = env
        self.opponent = opponent

    def reset(
        self,
        *,
        seed: Optional[int] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> Tuple[ObsType, Dict[str, Any]]:
        obs, infos = self.env.reset()
        return obs[self.env.agent1.username], infos[self.env.agent1.username]

    def step(
        self, action: ActionType
    ) -> Tuple[ObsType, float, bool, bool, Dict[str, Any]]:
        assert self.env.battle1 is not None
        opp_order = self.opponent.choose_move(self.env.battle1)
        assert not isinstance(opp_order, Awaitable)
        opp_action = self.env.order_to_action(opp_order, self.env.battle1)
        actions = {
            self.env.agent1.username: action,
            self.opponent.username: opp_action,
        }
        obs, rewards, terms, truncs, infos = self.env.step(actions)
        return (
            obs[self.env.agent1.username],
            rewards[self.env.agent1.username],
            terms[self.env.agent1.username],
            truncs[self.env.agent1.username],
            infos[self.env.agent1.username],
        )

    def render(self, mode="human"):
        return self.env.render(mode)

    def close(self):
        self.env.close()