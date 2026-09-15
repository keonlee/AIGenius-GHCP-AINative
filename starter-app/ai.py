"""Azure OpenAI-powered task tag suggestions."""

import logging
import re
from typing import Final

from azure_openai_client import (
    AzureOpenAIConfigurationError,
    create_azure_openai_client,
    load_azure_openai_config,
)

LOGGER = logging.getLogger(__name__)

SYSTEM_PROMPT: Final = (
    "Suggest one category tag for the task. Return a single lowercase tag "
    "containing only letters and numbers, with no spaces, punctuation, "
    "explanation, or formatting."
)
TAG_PATTERN: Final = re.compile(r"[a-z][a-z0-9]{0,49}")


def _extract_tag(response: object) -> str | None:
    """Extract a valid single tag from an Azure OpenAI response.

    Args:
        response: The chat completion response returned by the OpenAI client.

    Returns:
        A validated lowercase tag, or ``None`` for missing or malformed output.
    """
    choices = getattr(response, "choices", None)
    if not choices:
        return None
    message = getattr(choices[0], "message", None)
    content = getattr(message, "content", None)

    if not isinstance(content, str):
        return None

    tag = content.strip()
    if not TAG_PATTERN.fullmatch(tag):
        return None
    return tag


def suggest_tag(task_name: str, description: str) -> str | None:
    """Suggest a single category tag for a task using Azure OpenAI.

    Missing configuration, client errors, and malformed model responses are
    treated as optional-feature failures and return ``None`` so task creation
    can continue.

    Args:
        task_name: The task title to categorize.
        description: Optional additional task details.

    Returns:
        A validated lowercase tag, or ``None`` when no suggestion is available.
    """
    try:
        config = load_azure_openai_config()
    except AzureOpenAIConfigurationError:
        return None

    try:
        client = create_azure_openai_client(config)
        response = client.chat.completions.create(
            model=config.deployment,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        f"Task name: {task_name}\n"
                        f"Description: {description or '(none)'}"
                    ),
                },
            ],
            temperature=0,
            max_tokens=10,
        )
    except Exception as error:
        LOGGER.warning(
            "AI tag suggestion failed (%s). Saving without an AI tag.",
            type(error).__name__,
        )
        return None

    tag = _extract_tag(response)
    if tag is None:
        LOGGER.warning(
            "AI tag suggestion returned an invalid response. "
            "Saving without an AI tag."
        )
    return tag
