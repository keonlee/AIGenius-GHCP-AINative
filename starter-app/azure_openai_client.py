"""Azure OpenAI configuration and client construction."""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Final

from dotenv import load_dotenv
from openai import AzureOpenAI

AZURE_OPENAI_API_VERSION: Final = "2024-10-21"
AZURE_OPENAI_TIMEOUT_SECONDS: Final = 5.0
ENV_FILE: Final = Path(__file__).resolve().with_name(".env")

_ENDPOINT_ENV: Final = "AZURE_OPENAI_ENDPOINT"
_API_KEY_ENV: Final = "AZURE_OPENAI_API_KEY"
_DEPLOYMENT_ENV: Final = "AZURE_OPENAI_DEPLOYMENT"
_REQUIRED_ENV_VARS: Final = (
    _ENDPOINT_ENV,
    _API_KEY_ENV,
    _DEPLOYMENT_ENV,
)


class AzureOpenAIConfigurationError(RuntimeError):
    """Raised when required Azure OpenAI configuration is unavailable."""


@dataclass(frozen=True, slots=True)
class AzureOpenAIConfig:
    """Validated settings needed to call an Azure OpenAI deployment."""

    endpoint: str
    api_key: str = field(repr=False)
    deployment: str


def load_azure_openai_config() -> AzureOpenAIConfig:
    """Load and validate Azure OpenAI settings from the environment.

    A local ``.env`` file is loaded when present, without overriding variables
    already supplied by the process environment.

    Returns:
        Validated Azure OpenAI configuration.

    Raises:
        AzureOpenAIConfigurationError: If any required setting is missing.
    """
    load_dotenv(dotenv_path=ENV_FILE, override=False)
    values = {
        variable_name: (os.getenv(variable_name) or "").strip()
        for variable_name in _REQUIRED_ENV_VARS
    }
    missing_variables = [
        variable_name
        for variable_name, value in values.items()
        if not value
    ]
    if missing_variables:
        missing_list = ", ".join(missing_variables)
        raise AzureOpenAIConfigurationError(
            "Azure OpenAI configuration is incomplete. "
            f"Set the following environment variables: {missing_list}. "
            f"Define them in the process environment or in {ENV_FILE}."
        )

    return AzureOpenAIConfig(
        endpoint=values[_ENDPOINT_ENV],
        api_key=values[_API_KEY_ENV],
        deployment=values[_DEPLOYMENT_ENV],
    )


def create_azure_openai_client(
    config: AzureOpenAIConfig | None = None,
) -> AzureOpenAI:
    """Create a timeout-limited Azure OpenAI client.

    Args:
        config: Validated configuration. When omitted, configuration is loaded
            from environment variables and the local ``.env`` file.

    Returns:
        A configured Azure OpenAI client.

    Raises:
        AzureOpenAIConfigurationError: If required configuration is missing.
    """
    resolved_config = config or load_azure_openai_config()
    return AzureOpenAI(
        azure_endpoint=resolved_config.endpoint,
        api_key=resolved_config.api_key,
        api_version=AZURE_OPENAI_API_VERSION,
        timeout=AZURE_OPENAI_TIMEOUT_SECONDS,
    )
