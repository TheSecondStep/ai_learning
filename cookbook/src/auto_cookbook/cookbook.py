"""
This module is used to generate meal recipes based on provided ingredients using OpenAI API.
"""
import os
from dotenv import load_dotenv
from openai import OpenAI
from prompt_refiner import PromptRefiner


class RecipeRecommender:
    """
    A class used to recommend meal recipes based on provided ingredients using OpenAI API.

    This class initializes with API credentials and provides a method to generate recipes
    based on ingredients list, cuisine nationality, and number of servings.
    """

    def __init__(self, api_key: str = None, model: str = "deepseek-r1"):
        """
        Initialize the RecipeRecommender with an OpenAI client.

        Args:
            api_key (str, optional): Your OpenAI API key. Defaults to environment variable 'LLM_API_KEY'.
            model (str): The LLM model to use. Defaults to 'deepseek-r1'.
        """
        # 加载环境变量
        load_dotenv()

        # 初始化OpenAI客户端
        self.client = OpenAI(
            api_key=api_key or os.getenv("LLM_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )

        # 验证API密钥
        if not self.client.api_key:
            raise ValueError(
                "Missing LLM_API_KEY. Please set it in your environment or .env file.")

        self.model = model
        self.refiner = PromptRefiner(api_key=api_key)

        # 定义基础烹饪提示词模板
        self.base_prompt_template = """
        Generate {nationality} dishes while strictly adhering to these rules:
        1. Incorporate every provided ingredient and produce a number of dishes suitable for {person_number} people  
        2. Output exclusively in the official or most commonly spoken language of {nationality}
        3. Provide only the recipe name—omit cooking steps, quantities, and explanations
        4. Ensure each dish name authentically reflects {nationality}'s culinary style and typical ingredients
        """

    def cook_recommender(self, ingredients: list[str], nationality: str = "China", person_number: int = 1) -> str:
        """
        Generate a meal recipe using the provided ingredients list and OpenAI API.

        Args:
            ingredients (list[str]): A list of ingredients to use in the recipe.
            nationality (str): The nationality of the cuisine, defaults to "China".
            person_number (int): The number of servings, defaults to 1.

        Returns:
            str: A meal recipe tailored to the provided ingredients, cuisine nationality, and number of servings.
        """

        filtered_ingredients = [
            ingredient for ingredient in ingredients if ingredient.strip()]
        ingredients_text = ", ".join(filtered_ingredients)

        if not filtered_ingredients:
            return "Error: No ingredients provided. Please provide a list of ingredients."

        prompt = self.base_prompt_template.format(
            nationality=nationality,
            person_number=person_number
        ) + f"\n\nAvailable ingredients: {ingredients_text}"

        refined_prompt = self.refiner.refine(prompt, temperature=0.7)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional chef specializing in recipe creation."},
                    {"role": "user", "content": refined_prompt}
                ],
                temperature=0.7,
            )

            # 提取并返回生成的食谱
            recipe = response.choices[0].message.content
            return recipe

        except Exception as e:
            return f"Error generating recipe: {str(e)}"


if __name__ == "__main__":
    try:
        recommender = RecipeRecommender()

        example_foods = ["大米", "鸡肉", "土豆", "胡萝卜",
                         "鸡蛋", "番茄", "青菜", "豆腐", "牛肉", "西兰花"]

        if not example_foods:
            example_foods = ["鸡蛋", "番茄", "米饭"]

        print("生成中餐食谱（2人份）...")
        chinese_recipe = recommender.cook_recommender(
            example_foods[:5], nationality="China", person_number=2)
        print(chinese_recipe)

        print("\n" + "="*50 + "\n")

        print("生成美式食谱（1人份）...")
        western_recipe = recommender.cook_recommender(
            example_foods[5:10], nationality="America", person_number=1)
        print(western_recipe)

    except Exception as e:
        print(f"程序运行出错: {str(e)}")
