"""
config_loader.py — Singleton config with ${ENV_VAR} resolution.

Loads environment YAML, resolves ${VARIABLE} placeholders from .env,
and returns a fully populated config dict. Cached per-session.
"""

import os
import re
import yaml
from pathlib import Path
from dotenv import load_dotenv

from config.settings import ENVIRONMENTS_DIR, ENV_FILE

# Load .env once at module import
load_dotenv(dotenv_path=ENV_FILE)

ENV_VAR_PATTERN = re.compile(r"\$\{([A-Z_][A-Z0-9_]*)\}")


class ConfigLoader:
    """
    Singleton loader for environment-specific YAML configuration.
    Resolves ${ENV_VAR} patterns against values in .env file.
    """

    _instance = None
    _cache = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load(self, env: str) -> dict:
        """
        Loads the YAML config for the given environment.
        Returns a dict with all ${ENV_VAR} values resolved from .env.

        Args:
            env: Environment name ('dev', 'uat', 'prod', etc.)

        Returns:
            Fully resolved config dict
        """
        if env in self._cache:
            return self._cache[env]

        yaml_path = ENVIRONMENTS_DIR / f"{env}.yaml"
        if not yaml_path.exists():
            raise FileNotFoundError(
                f"Environment config not found: {yaml_path}\n"
                f"Create config/environments/{env}.yaml or use a different --env flag"
            )

        with open(yaml_path, "r", encoding="utf-8") as f:
            raw = yaml.safe_load(f) or {}

        resolved = self._resolve_env_vars(raw)
        self._cache[env] = resolved
        return resolved

    def _resolve_env_vars(self, obj):
        """Recursively replaces ${VAR} tokens with values from environment."""
        if isinstance(obj, dict):
            return {k: self._resolve_env_vars(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._resolve_env_vars(item) for item in obj]
        if isinstance(obj, str):
            return ENV_VAR_PATTERN.sub(
                lambda m: os.environ.get(m.group(1), ""), obj
            )
        return obj

    def clear_cache(self):
        """Clear the config cache. Primarily used for testing."""
        self._cache.clear()
