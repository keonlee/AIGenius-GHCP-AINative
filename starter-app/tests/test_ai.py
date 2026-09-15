"""Tests for Azure OpenAI tag suggestions and CLI integration."""

import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from click.testing import CliRunner

import ai
import app
import azure_openai_client


AZURE_OPENAI_ENVIRONMENT = {
    "AZURE_OPENAI_ENDPOINT": "https://example.openai.azure.com",
    "AZURE_OPENAI_API_KEY": "test-api-key",
    "AZURE_OPENAI_DEPLOYMENT": "test-deployment",
}


@pytest.fixture(autouse=True)
def isolated_azure_openai_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure tests never inherit real Azure OpenAI credentials."""
    for variable_name in AZURE_OPENAI_ENVIRONMENT:
        monkeypatch.delenv(variable_name, raising=False)


def configure_azure_openai(monkeypatch: pytest.MonkeyPatch) -> None:
    """Set non-secret test values for all required Azure OpenAI settings."""
    for variable_name, value in AZURE_OPENAI_ENVIRONMENT.items():
        monkeypatch.setenv(variable_name, value)


def model_response(content: str | None) -> SimpleNamespace:
    """Build the minimal response shape returned by chat completions."""
    return SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=content))]
    )


class TestSuggestTag:
    def test_returns_valid_tag_and_sends_constrained_prompt(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        configure_azure_openai(monkeypatch)
        client = MagicMock()
        client.chat.completions.create.return_value = model_response("devops")
        client_factory = MagicMock(return_value=client)
        monkeypatch.setattr(ai, "create_azure_openai_client", client_factory)

        result = ai.suggest_tag("Deploy to production", "Run the release pipeline")

        assert result == "devops"
        client_factory.assert_called_once()
        config = client_factory.call_args.args[0]
        assert config.endpoint == AZURE_OPENAI_ENVIRONMENT["AZURE_OPENAI_ENDPOINT"]
        assert config.api_key == AZURE_OPENAI_ENVIRONMENT["AZURE_OPENAI_API_KEY"]
        assert config.deployment == AZURE_OPENAI_ENVIRONMENT[
            "AZURE_OPENAI_DEPLOYMENT"
        ]

        completion_arguments = client.chat.completions.create.call_args.kwargs
        assert completion_arguments["model"] == AZURE_OPENAI_ENVIRONMENT[
            "AZURE_OPENAI_DEPLOYMENT"
        ]
        messages = completion_arguments["messages"]
        system_prompt = next(
            message["content"] for message in messages if message["role"] == "system"
        )
        user_prompt = next(
            message["content"] for message in messages if message["role"] == "user"
        )
        assert "single" in system_prompt.lower()
        assert "lowercase" in system_prompt.lower()
        assert "Deploy to production" in user_prompt
        assert "Run the release pipeline" in user_prompt

    @pytest.mark.parametrize("missing_variable", AZURE_OPENAI_ENVIRONMENT)
    def test_returns_none_when_configuration_is_incomplete(
        self,
        monkeypatch: pytest.MonkeyPatch,
        missing_variable: str,
    ) -> None:
        configure_azure_openai(monkeypatch)
        monkeypatch.delenv(missing_variable)
        client_factory = MagicMock()
        monkeypatch.setattr(ai, "create_azure_openai_client", client_factory)

        assert ai.suggest_tag("Deploy", "") is None
        client_factory.assert_not_called()

    @pytest.mark.parametrize(
        "content",
        [
            None,
            "",
            "   ",
            "devops, cloud",
            "two words",
            "DevOps!",
        ],
    )
    def test_returns_none_for_empty_or_malformed_model_output(
        self,
        monkeypatch: pytest.MonkeyPatch,
        content: str | None,
    ) -> None:
        configure_azure_openai(monkeypatch)
        client = MagicMock()
        client.chat.completions.create.return_value = model_response(content)
        monkeypatch.setattr(
            ai,
            "create_azure_openai_client",
            MagicMock(return_value=client),
        )

        assert ai.suggest_tag("Deploy", "") is None

    def test_returns_none_for_response_without_choices(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        configure_azure_openai(monkeypatch)
        client = MagicMock()
        client.chat.completions.create.return_value = SimpleNamespace(choices=[])
        monkeypatch.setattr(
            ai,
            "create_azure_openai_client",
            MagicMock(return_value=client),
        )

        assert ai.suggest_tag("Deploy", "") is None

    def test_returns_none_when_api_call_fails(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        configure_azure_openai(monkeypatch)
        client = MagicMock()
        client.chat.completions.create.side_effect = RuntimeError("service unavailable")
        monkeypatch.setattr(
            ai,
            "create_azure_openai_client",
            MagicMock(return_value=client),
        )

        assert ai.suggest_tag("Deploy", "") is None


class TestAzureOpenAIClientSetup:
    def test_loads_required_configuration(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        configure_azure_openai(monkeypatch)

        config = azure_openai_client.load_azure_openai_config()

        assert config.endpoint == AZURE_OPENAI_ENVIRONMENT["AZURE_OPENAI_ENDPOINT"]
        assert config.api_key == AZURE_OPENAI_ENVIRONMENT["AZURE_OPENAI_API_KEY"]
        assert config.deployment == AZURE_OPENAI_ENVIRONMENT[
            "AZURE_OPENAI_DEPLOYMENT"
        ]
        assert AZURE_OPENAI_ENVIRONMENT["AZURE_OPENAI_API_KEY"] not in repr(config)

    @pytest.mark.parametrize("missing_variable", AZURE_OPENAI_ENVIRONMENT)
    def test_missing_configuration_raises_actionable_error(
        self,
        monkeypatch: pytest.MonkeyPatch,
        missing_variable: str,
    ) -> None:
        configure_azure_openai(monkeypatch)
        monkeypatch.delenv(missing_variable)

        with pytest.raises(
            azure_openai_client.AzureOpenAIConfigurationError,
            match=missing_variable,
        ):
            azure_openai_client.load_azure_openai_config()

    def test_creates_timeout_limited_azure_client(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        config = azure_openai_client.AzureOpenAIConfig(
            endpoint=AZURE_OPENAI_ENVIRONMENT["AZURE_OPENAI_ENDPOINT"],
            api_key=AZURE_OPENAI_ENVIRONMENT["AZURE_OPENAI_API_KEY"],
            deployment=AZURE_OPENAI_ENVIRONMENT["AZURE_OPENAI_DEPLOYMENT"],
        )
        client_factory = MagicMock()
        monkeypatch.setattr(azure_openai_client, "AzureOpenAI", client_factory)

        azure_openai_client.create_azure_openai_client(config)

        client_factory.assert_called_once_with(
            azure_endpoint=config.endpoint,
            api_key=config.api_key,
            api_version=azure_openai_client.AZURE_OPENAI_API_VERSION,
            timeout=5,
        )


class TestAddCommandAiIntegration:
    def test_add_uses_and_displays_suggested_tag(
        self,
        isolated_tasks_file: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        suggest_tag = MagicMock(return_value="devops")
        monkeypatch.setattr(app, "suggest_tag", suggest_tag)

        result = CliRunner().invoke(
            app.cli,
            ["add", "Deploy", "--description", "Run the release pipeline"],
        )

        assert result.exit_code == 0
        suggest_tag.assert_called_once_with("Deploy", "Run the release pipeline")
        tasks = json.loads(isolated_tasks_file.read_text(encoding="utf-8"))
        assert tasks[0]["tags"] == ["devops"]
        assert "AI suggested tag: devops" in result.output

    def test_explicit_tag_skips_ai(
        self,
        isolated_tasks_file: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        suggest_tag = MagicMock()
        monkeypatch.setattr(app, "suggest_tag", suggest_tag)

        result = CliRunner().invoke(app.cli, ["add", "Deploy", "--tag", "release"])

        assert result.exit_code == 0
        suggest_tag.assert_not_called()
        tasks = json.loads(isolated_tasks_file.read_text(encoding="utf-8"))
        assert tasks[0]["tags"] == ["release"]

    def test_no_ai_flag_skips_suggestion(
        self,
        isolated_tasks_file: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        suggest_tag = MagicMock()
        monkeypatch.setattr(app, "suggest_tag", suggest_tag)

        result = CliRunner().invoke(app.cli, ["add", "Deploy", "--no-ai"])

        assert result.exit_code == 0
        suggest_tag.assert_not_called()
        tasks = json.loads(isolated_tasks_file.read_text(encoding="utf-8"))
        assert tasks[0]["tags"] == []

    def test_missing_configuration_does_not_block_add(
        self,
        isolated_tasks_file: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        suggest_tag = MagicMock(return_value=None)
        monkeypatch.setattr(app, "suggest_tag", suggest_tag)

        result = CliRunner().invoke(app.cli, ["add", "Deploy"])

        assert result.exit_code == 0
        suggest_tag.assert_called_once_with("Deploy", "")
        tasks = json.loads(isolated_tasks_file.read_text(encoding="utf-8"))
        assert tasks[0]["tags"] == []
        assert "Added task" in result.output
        assert "AI suggested tag:" not in result.output

    def test_unexpected_ai_error_is_visible_and_does_not_block_add(
        self,
        isolated_tasks_file: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        suggest_tag = MagicMock(side_effect=RuntimeError("test-api-key"))
        monkeypatch.setattr(app, "suggest_tag", suggest_tag)

        result = CliRunner().invoke(app.cli, ["add", "Deploy"])

        assert result.exit_code == 0
        tasks = json.loads(isolated_tasks_file.read_text(encoding="utf-8"))
        assert tasks[0]["tags"] == []
        assert "AI tag suggestion failed" in result.output
        assert "test-api-key" not in result.output

    def test_no_ai_flag_is_documented(self) -> None:
        result = CliRunner().invoke(app.cli, ["add", "--help"])

        assert result.exit_code == 0
        assert "--no-ai" in result.output
