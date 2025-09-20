"""
Test script for the PromptRefiner class.
This script demonstrates how to use the PromptRefiner to refine a sample prompt
"""

from redlines import Redlines
from src.prompt_refiner import PromptRefiner


def run_test():
    refiner = PromptRefiner()

    PROMPT = """
    You are an AI program assistant designed to recommend cookbook by the food that's inputed by the user.
    You respond in a short, very conversational friendly style.
    """
    refined_prompt = refiner.refine(PROMPT)

    test = Redlines(PROMPT, refined_prompt, markdown_style="none")
    print(test.output_markdown)  # Print the diff in markdown format


if __name__ == "__main__":
    run_test()
