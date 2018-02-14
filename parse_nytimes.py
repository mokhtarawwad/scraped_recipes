import os
from scrapy.selector import Selector

XPATH_RECIPE_NAME = '//*[@itemprop="name"]/text()'
XPATH_RECIPE_AUTHOR = '//*[@itemprop="author"]/text()'
XPATH_RECIPE_YIELD = '//*[@itemprop="recipeYield"]/text()'
XPATH_RECIPE_COOKING_TIME = '//*[@itemprop="cookTime"]/@content'

# Get the directory that contains the raw recipe data
for text_file in os.listdir("./nytimes"):
    # Print the text file name
    #print(text_file)
    
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
    if recipe_cooking_time:
        recipe_cooking_time = recipe_cooking_time[0]
    print(recipe_cooking_time)
    
    
    # Parse for all the recipe ingredients
    # Parse for the nutrition information
    # Parse for the recipe instructions

    # Then syntesize all that data into a tuple or document
    # And save it to a database
