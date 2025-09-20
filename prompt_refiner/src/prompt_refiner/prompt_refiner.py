"""
Prompt Refiner Module
---------------------
This module refines and optimizes prompts using a large language model (LLM)
powered by https://www.aliyun.com/product/bailian.

Features:
- PromptRefiner.refine(prompt): Refine any given prompt.
- PromptRefiner.refine_system_prompt(): Refine the built-in SYSTEM_PROMPT itself.

The SYSTEM_PROMPT is private and encapsulated; users interact with it only via
the class methods.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI


class PromptRefiner:
    """
    Class to refine and optimize prompts using an LLM.

    Attributes:
        _SYSTEM_PROMPT (str): The default system instructions guiding prompt refinement.
        client (OpenAI): The LLM client instance.
        model (str): Model name used for refinement.
    """

    # ---------------------------
    # Private system prompt
    # ---------------------------
    _SYSTEM_PROMPT = """
    You are an AI program assistant designed to proofread and optimize English texts
    for use as prompts in other LLM assistants. Your task is to improve the clarity,
    specificity, and overall effectiveness of the provided text while maintaining
    the original meaning.

    Your responsibilities include:

    1. Correcting Grammar and Spelling: Fix any grammatical or spelling errors.
    2. Improving Clarity: Simplify and reorganize sentences for easy understanding.
    3. Enhancing Specificity: Make the instructions or queries more precise.
    4. Optimizing for Prompt Effectiveness:
        a. Be direct and clear.
        b. Provide context when needed.
        c. Avoid ambiguity and vagueness.
        d. Define terms or instructions explicitly if necessary.

    The output should only contain the optimized prompt without any additional
    commentary or explanation.
    """

    def __init__(self, api_key: str = None, model: str = "deepseek-r1"):
        """
        Initialize the PromptRefiner with an LLM client.

        Args:
            api_key (str, optional): Your LLM API key. Defaults to environment variable 'LLM_API_KEY'.
            model (str): The LLM model to use. Defaults to 'deepseek-r1'.
        """
        load_dotenv()
        self.client = OpenAI(
            api_key=api_key or os.getenv("LLM_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        if not self.client.api_key:
            raise ValueError(
                "Missing LLM_API_KEY. Please set it in your environment or .env file.")
        self.model = model

    def refine(
        self,
        prompt: str,
        system_prompt: str = None,
        temperature: float = 0
    ) -> str:
        """
        Refine the given prompt using the LLM.

        Args:
            prompt (str): The user input prompt to refine.
            system_prompt (str, optional): The system instructions guiding refinement. Defaults to the private SYSTEM_PROMPT.
            temperature (float): Sampling temperature for creativity control (default: 0).

        Returns:
            str: The refined prompt.
        """
        system_prompt = system_prompt or self._SYSTEM_PROMPT
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
        )
        return completion.choices[0].message.content

    def refine_system_prompt(self, temperature: float = 0) -> str:
        """
        Refine the built-in SYSTEM_PROMPT itself using the LLM.

        Args:
            temperature (float): Sampling temperature for creativity control (default: 0).

        Returns:
            str: The refined SYSTEM_PROMPT.
        """
        return self.refine(self._SYSTEM_PROMPT, self._SYSTEM_PROMPT, temperature)
