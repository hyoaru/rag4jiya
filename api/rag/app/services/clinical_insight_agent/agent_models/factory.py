from typing import cast
from pydantic_ai.models.openai import OpenAIModel, OpenAIModelName
from pydantic_ai.providers.openai import OpenAIProvider

from app.common.configs import EnvironmentConfig


class AgentModelFactory:
    @staticmethod
    def create(model: str):
        environment_config = EnvironmentConfig()

        match model:
            case "openai":
                return OpenAIModel(
                    model_name=cast(
                        OpenAIModelName,
                        environment_config.OPENAI_INFERENCE_MODEL,
                    ),
                    provider=OpenAIProvider(
                        api_key=environment_config.OPENAI_API_KEY,
                    ),
                )
