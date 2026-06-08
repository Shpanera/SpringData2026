from __future__ import annotations

from copy import deepcopy

from ..config import RuntimeConfig


class RuntimeConfigService:
    def __init__(self, initial_config: RuntimeConfig) -> None:
        self._config = initial_config

    def get(self) -> RuntimeConfig:
        return deepcopy(self._config)

    def update(self, payload: RuntimeConfig) -> RuntimeConfig:
        self._config = payload
        return self.get()
