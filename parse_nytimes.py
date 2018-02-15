import os
import pprint
from scrapy.selector import Selector

XPATH_RECIPE_NAME = '//*[@itemprop="name"]/text()'
XPATH_RECIPE_AUTHOR = '//*[@itemprop="author"]/text()'
XPATH_RECIPE_YIELD = '//*[@itemprop="recipeYield"]/text()'
XPATH_RECIPE_COOKING_TIME = '//*[@itemprop="cookTime"]/@content'
XPATH_RECIPE_INGREDIENTS = '//*[@itemprop="recipeIngredient"]'
XPATH_INGREDIENT_QUANTITY = '//*[@class="quantity"]/text()'
XPATH_INGREDIENT_PRE_DESC = '//*[@class="ingredient-name"]/text()'
XPATH_INGREDIENT_CORE_ELEMENT = '//*[@class="ingredient-name"]/span/text()'
XPATH_INGREDIENT_POST_DESC = '//*[@class="ingredient-name"]/span/following-sibling::text()[1]'


# Get the directory that contains the raw recipe data
for text_file in os.listdir("./nytimes"):
    # Print the text file name
    print(text_file)
    
    # Then for every file in that directory
    recipe_file = open(os.path.join(os.getcwd(), "nytimes", text_file), "r").read()
    
    # PARSE FOR NAME
    recipe_name = Selector(text=recipe_file).xpath(XPATH_RECIPE_NAME).extract()
    # Then clean it up by stripping it of whitespace
    recipe_name = recipe_name[0].strip()
    print(recipe_name)
    
    
    # PARSE FOR AUTHOR
    recipe_author = Selector(text=recipe_file).xpath(XPATH_RECIPE_AUTHOR).extract()
    if recipe_author:
        recipe_author = recipe_author[0]
    #print(recipe_author)
    
    
    # PARSE FOR RECIPE YIELD
    recipe_yield = Selector(text=recipe_file).xpath(XPATH_RECIPE_YIELD).extract()
    if recipe_yield:
        recipe_yield = recipe_yield[0]
    #print(recipe_yield)
    
    
    # PARSE FOR COOKING TIME
    recipe_cooking_time = Selector(text=recipe_file).xpath(XPATH_RECIPE_COOKING_TIME).extract()
    #quantity, ingredientName/span
    if recipe_cooking_time:
        recipe_cooking_time = recipe_cooking_time[0]
    #print(recipe_cooking_time)
    
    
    # PARSE FOR INGREDIENTS
    recipe_ingredients_html = Selector(text=recipe_file).xpath(XPATH_RECIPE_INGREDIENTS).extract()
    recipe_ingredients = []
    for item in recipe_ingredients_html:
        ingredient_text = ""
        quantity = Selector(text=item).xpath(XPATH_INGREDIENT_QUANTITY).extract()
        before_text = Selector(text=item).xpath(XPATH_INGREDIENT_PRE_DESC).extract()
        core_food_item = Selector(text=item).xpath(XPATH_INGREDIENT_CORE_ELEMENT).extract()
        after_text = Selector(text=item).xpath(XPATH_INGREDIENT_POST_DESC).extract()
        if quantity:
            ingredient_text += quantity[0].strip()
        if before_text:
            ingredient_text += " " + before_text[0].strip()
        if core_food_item:
            ingredient_text += " " + food_item[0].strip()
        if after_text:
            ingredient_text += " " + after_text[0].strip()
        # Remove extra spaces
        # TODO -- remove extra spaces like " , "
        ingredient_text = " ".join(ingredient_text.split())
        recipe_ingredients.append(ingredient_text)
    pprint.pprint(recipe_ingredients)
        
    
    
    # Parse for the nutrition information
    # Parse for the recipe instructions

    # Then syntesize all that data into a tuple or document
    # And save it to a database
