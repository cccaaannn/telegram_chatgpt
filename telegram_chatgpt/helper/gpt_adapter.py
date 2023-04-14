from typing import Any
import logging
import os

import openai

from exception.gpt_prediction_exception import GPTPredictionException
from util.env_utils import ConfigEnvNames


class GPTAdapter():
    def __init__(self) -> None:
        openai.api_key = os.getenv(ConfigEnvNames.OPENAI_API_ENVIRONMENT_NAME.value)
        self.__logger = logging.getLogger(self.__class__.__name__)
        self.__gpt_model = os.getenv(ConfigEnvNames.GPT_MODEL.value)

    async def inference(self, message_history) -> Any:
        try:
            completion = await openai.ChatCompletion.acreate(
                model=self.__gpt_model,
                messages=message_history
            )
            return completion.choices[0].message.content
        except:
            self.__logger.error("Could not predict", exc_info=True)
            raise GPTPredictionException()
