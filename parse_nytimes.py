import json
import logging
import os
import pprint
import re
from pymongo import MongoClient
from scrapy.selector import Selector

client_mongo = MongoClient('mongodb://michael:secretPassword@mike-wheeler.io/recipeInfo');


RECIPE_DIRECTORY = "./nytimes"
XPATH_RECIPE_NAME = '//*[@itemprop="name"]/text()'
XPATH_RECIPE_AUTHOR = '//*[@itemprop="author"]/text()'
XPATH_RECIPE_YIELD = '//*[@itemprop="recipeYield"]/text()'
XPATH_RECIPE_COOKING_TIME = '//*[@itemprop="cookTime"]/@content'
XPATH_RECIPE_INGREDIENTS = '//*[@itemprop="recipeIngredient"]'
XPATH_INGREDIENT_QUANTITY = '//*[@class="quantity"]/text()'
XPATH_INGREDIENT_PRE_DESC = '//*[@class="ingredient-name"]/text()'
XPATH_INGREDIENT_CORE_ELEMENT = '//*[@class="ingredient-name"]/span/text()'
XPATH_INGREDIENT_POST_DESC = '//*[@class="ingredient-name"]/span/following-sibling::text()[1]'
XPATH_CALORIES = '//*[@itemprop="calories"]/text()'
XPATH_FAT_CONTENT = '//*[@itemprop="fatContent"]/text()'
XPATH_SATURATED_FAT_CONTENT = '//*[@itemprop="saturatedFatContent"]/text()'
XPATH_TRANS_FAT_CONTENT = '//*[@itemprop="transFatContent"]/text()'
XPATH_CARBOHYDRATE_CONTENT = '//*[@itemprop="carbohydrateContent"]/text()'
XPATH_FIBER_CONTENT = '//*[@itemprop="fiberContent"]/text()'
XPATH_PROTEIN_CONTENT = '//*[@itemprop="proteinContent"]/text()'
XPATH_CHOLESTEROL_CONTENT = '//*[@itemprop="cholesterolContent"]/text()'
XPATH_SODIUM_CONTENT = '//*[@itemprop="sodiumContent"]/text()'
XPATH_RECIPE_DIRECTIONS = '//*[@itemprop="recipeInstructions"]/li/text()'

class Recipe:
    """
    Contains all the recipe data scraped out of the articles.
    Used to automate the storage of recipes in the target database system
    with pre-defined methods.
    """

    def __init__(self, name, fileName, author, recipeYield, cookTime, ingredients,
                 nutrition, directions, originalText, source="https://cooking.nytimes.com/"):
        self.name = name
        self.fileName = fileName
        self.author = author
        self.recipeYield = recipeYield
        self.cookTime = cookTime
        self.ingredients = ingredients
        self.nutrition = nutrition
        self.directions = directions
        self.originalText = originalText
        self.source = source
        
    def __str__(self):
        return self.__dict__;
   
    def as_dict(self):
        """
        Returns a dictionary representation of the Recipe class
        """
        returnValue = dict()
        if self.name:
            returnValue["name"] = self.name
        if self.fileName:
            returnValue["fileName"] = self.fileName
        if self.author:
            returnValue["author"] = self.author
        if self.recipeYield:
            try:
                returnValue["yield"] = self.recipeYield.as_dict()
            except AttributeError:
                returnValue["yield"] = self.recipeYield
        if self.cookTime:
            returnValue["cookTime"] = self.cookTime.as_dict()
        if self.ingredients:
            returnValue["ingredients"] = self.ingredients
        if self.nutrition:
            returnValue["nutrition"] = self.nutrition.as_dict()
        if self.directions:
            returnValue["directions"] = self.directions
        if self.source:
            returnValue["source"] = self.source
        return returnValue
        
       
    def writeToMySQL(self, connection):
        """
        Writes the structured object data to a MySQL database.
        """
        pass  # TODO -- write
       
    def writeToMongoDB(self, connection):
        """
        Writes the structured object data to a MongoDB database.
        """
        db = connection.recipeInfo
        recipe_collection = db.recipes
        result = recipe_collection.insert_one(self.as_dict())
        print(result)  # TODO -- handle success and failure
        
class Ingredient:
    def __init__(self, quantity, food_item, modifiers):
        self.quantity = quantity
        self.food_item = food_item
        self.modifiers = modifiers
        
    def __str__(self):
        return str(quantity) + "FOOD: " + self.food_item + "MODIFIERS: " + self.modifiers
        
    def as_dict(self):
        """
        Returns a dictionary representation of the Ingredient class
        """
        returnValue = dict()
        if self.quantity:
            returnValue["quantity"] = self.quantity.as_dict()
        if self.food_item:
            returnValue["foodItem"] = self.food_item
        if self.modifiers:
            returnValue["modifiers"] = self.modifiers
        return returnValue
        
class RecipeNutrition:
    """
    Describes the Nutrition Facts table for a recipe, where each attribute
    is an instance of Measurement.
    """
    def __init__(self, calories, total_fat, saturated_fat, trans_fat, 
                 carbs, fiber, protein, cholesterol, sodium):
        self.calories = calories
        self.total_fat = total_fat
        self.saturated_fat = saturated_fat
        self.trans_fat = trans_fat
        self.carbs = carbs
        self.fiber = fiber
        self.protein = protein
        self.cholesterol = cholesterol
        self.sodium = sodium
        
    def as_dict(self):
        """
        Returns a dictionary representation of the RecipeNutrition class
        """
        returnValue = list()
        if self.calories:
            returnValue.append(self.calories.as_dict())
        if self.total_fat:
            returnValue.append(self.total_fat.as_dict())
        if self.saturated_fat:
            returnValue.append(self.saturated_fat.as_dict())
        if self.trans_fat:
            returnValue.append(self.trans_fat.as_dict())
        if self.carbs:
            returnValue.append(self.carbs.as_dict())
        if self.fiber:
            returnValue.append(self.fiber.as_dict())
        if self.protein:
            returnValue.append(self.protein.as_dict())
        if self.cholesterol:
            returnValue.append(self.cholesterol.as_dict())
        if self.sodium:
            returnValue.append(self.sodium.as_dict())
        return returnValue
       

class NutritionFact:
    """
    Describes a statement about the nutritional value of a Recipe.
    """
    def __init__(self, measurement, substance):
        self.measurement = measurement
        self.substance = substance
        
    def as_dict(self):
        """
        Returns a dictionary representation of the NutritionFact class
        """
        returnValue = dict()
        if self.measurement:
            returnValue["measurement"] = self.measurement.as_dict()
        if self.substance:
            returnValue["substance"] = self.substance
        return returnValue


class Measurement:
   """
   Describes a pairing of a positive number and a unit of measurement.
   Used to describe the quantity of an ingredient, nutrition facts, or 
   an amount of time to cook.
   """
   def __init__(self, quantity, unit):
       self.quantity = float(quantity)
       self.unit = unit
       
   def __str__(self):
       return "QTY: " + str(self.quantity) + ", UNIT: " + str(self.unit)
       
   def as_dict(self):
        """
        Returns a dictionary representation of the RecipeNutrition class
        """
        returnValue = dict()
        if self.quantity:
            returnValue["quantity"] = self.quantity
        if self.unit:
            returnValue["unit"] = self.unit
        return returnValue
       
       
def parse_markup(markup, xpath):
    """
    Convenience function for parsing some markup with a given XPath statement.
    """
    return Selector(text=markup).xpath(xpath).extract()
    
def handle_fractions(qty):
    """
    Converts Strings containing Unicode fractions into actual numbers
    """ 
    
    if not qty:
        return 0
    
    known_unicode_fractions = {u"⅞": float(7/8), 
                               u"⅝": float(5/8),
                               u"⅜": float(3/8),
                               u"⅛": float(1/8),
                               u"⅚": float(5/6),
                               u"⅙": float(1/6),
                               u"⅘": float(4/5),
                               u"⅗": float(3/5),
                               u"⅖": float(2/5),
                               u"⅕": float(1/5),
                               u"⅔": float(2/3),
                               u"⅓": float(1/3),
                               u"⅒": float(1/10),
                               u"⅑": float(1/9),
                               u"⅐": float(1/7),
                               u"¾": float(3/4),
                               u"½": float(1/2),
                               u"¼": float(1/4),
                               u"↉": 0}
    superscripts = {u"⁰": 0,
                    u"¹": 1,
                    u"²": 2,
                    u"³": 3,
                    u"⁴": 4,
                    u"⁵": 5,
                    u"⁶": 6,
                    u"⁷": 7,
                    u"⁸": 8,
                    u"⁹": 9,
                   }
    subscripts = {u"₀": 0,
                  u"₁": 1,
                  u"₂": 2,
                  u"₃": 3,
                  u"₄": 4,
                  u"₅": 5,
                  u"₆": 6,
                  u"₇": 7,
                  u"₈": 8,
                  u"₉": 9,
                 }
    fraction_slash = u"⁄"
    numerator_one_character = u"⅟"
    early_warning_characters = ["⅞", "⅝", "⅜", "⅛", "⅚", "⅙", 
                                "⅘", "⅗", "⅖", "⅕", "⅔", "⅓", 
                                "⅒", "⅑", "⅐", "¾", "½", "¼", 
                                "↉", ]
    regex_prefix = "(\d+)+"
    regex_dumb_simple_fraction = "(\d+)/(\d+)"
    regex_dumb_mixed_number = "(\d+) ((\d+)/(\d+))"
    regex_fraction_characters = "([⅞⅝⅜⅛⅚⅙⅘⅗⅖⅕⅔⅓⅒⅑⅐¾½¼↉])"
    regex_numerator_one_fraction = numerator_one_character + "([₀₁₂₃₄₅₆₇₈₉]+)"
    regex_fraction_general = "([⁰¹²³⁴⁵⁶⁷⁸⁹]+)" + fraction_slash + "([₀₁₂₃₄₅₆₇₈₉]+)"
    regex_mixed_number_fraction_characters = regex_prefix + regex_fraction_characters
    regex_mixed_number_numerator_one = regex_prefix + regex_numerator_one_fraction
    regex_mixed_number_general = regex_prefix + regex_fraction_general
    
    # First check if it's a fraction in dumb notation ("1/2")
    match = re.match(regex_dumb_simple_fraction, qty)
    if match:
        num = float(match.group(1))
        denom = float(match.group(2))
        return num/denom
    
    # Then check if it's a mixed number in dumb notation
    match = re.match(regex_dumb_mixed_number, qty)
    if match:
        whole_part = float(match.group(1))
        num = float(match.group(3))
        denom = float(match.group(4))
        return float(whole_part + num/denom)
    
    # Remove all whitespace to make regex matching easier
    qty = qty.replace(" ","").replace("\n", "").replace("\t", "").replace("\r", "")
    
    # Check to see if it's a mixed number with the fraction character         
    match = re.match(regex_mixed_number_fraction_characters, qty)
    if match:
        whole_part = float(match.group(1))
        fractional_part = known_unicode_fractions[match.group(2)]
        return whole_part + fractional_part
    
    # Check to see if it's a mixed number with the 1-over character
    match = re.match(regex_mixed_number_numerator_one, qty)
    if match:
        whole_part = float(match.group(1))
        list_of_denominator_digits = list(match.group(2))
        denom = 0
        for char in list_of_denominator_digits:
            denom = 10*denom + subscripts[char]
        return whole_part + (1/denom)
    
    # Check to see if it's a mixed number with the Unicode fraction slash
    match = re.match(regex_mixed_number_general, qty)
    if match:
        whole_part = float(match.group(1))
        list_of_numerator_digits = list(match.group(2))
        list_of_denominator_digits = list(match.group(3))
        num = 0
        for char in list_of_numerator_digits:
            num = 10*num + superscripts[char]
        denom = 0
        for char in list_of_denominator_digits:
            denom = 10*denom + subscripts[char]
        return whole_part + (num/denom)
        
    # Check to see if it's just a fraction character         
    match = re.match(regex_fraction_characters, qty)
    if match:
        fractional_part = known_unicode_fractions[match.group(1)]
        return fractional_part
    
    # Check to see if it's just a fraction with the 1-over character
    match = re.match(regex_numerator_one_fraction, qty)
    if match:
        list_of_denominator_digits = list(match.group(1))
        denom = 0
        for char in list_of_denominator_digits:
            denom = 10*denom + subscripts[char]
        return (1/denom)
    
    # Check to see if it's just a fraction with the Unicode fraction slash
    match = re.match(regex_fraction_general, qty)
    if match:
        list_of_numerator_digits = list(match.group(1))
        list_of_denominator_digits = list(match.group(2))
        num = 0
        for char in list_of_numerator_digits:
            num = 10*num + superscripts[char]
        denom = 0
        for char in list_of_denominator_digits:
            denom = 10*denom + subscripts[char]
        return (num/denom)
   
    # Check to see if it's just digits
    match = re.match(regex_prefix, qty)
    if match:
        try:
            return float(match.group(1))
        except:
            raise Exception("Cannot parse this form: " + qty)
    else:  # Otherwise give up
        raise Exception("Cannot parse the form: " + qty)
        
        
        
# Tests for this function
assert(handle_fractions("0") == 0)
assert(handle_fractions("1") == 1)
assert(handle_fractions("2") == 2)
assert(handle_fractions("03") == 3)
assert(handle_fractions("1/4") == 0.25)
assert(handle_fractions("¼") == 0.25)
assert(handle_fractions("7/8") == 0.875)
assert(handle_fractions("⅞") == 0.875)
assert(handle_fractions("2 1/4") == 2.25)
assert(handle_fractions("2 ¼") == 2.25)
assert(handle_fractions("21/4") == 5.25)
assert(handle_fractions("12 7/8") == 12.875)
assert(handle_fractions("12 ⅞") == 12.875)
assert(handle_fractions("127/8") == 15.875)
assert(handle_fractions("⅟₂₅") == 0.04)
assert(handle_fractions("1/25") == 0.04)
assert(handle_fractions("9 ⅟₈") == 9.125)
assert(handle_fractions("9 1/8") == 9.125)
assert(handle_fractions("³⁄₂₅") == 0.12)
assert(handle_fractions("3/25") == 0.12)
assert(handle_fractions("⁵⁄₂₅₀₀") == 0.002)
assert(handle_fractions("5/2500") == 0.002)
assert(handle_fractions("9 ⁷⁄₈") == 9.875)
assert(handle_fractions("9 7/8") == 9.875)


def make_nutrition(xpath_output, calories=False):
    """
    Takes in the result of parsing the Nutrition information and returns a Measurement.
    If calories, just strip the number; else split on the string
    """
    if xpath_output:
        if calories:
            return Measurement(float(xpath_output[0]), "calories")
        else:
            measure_info = xpath_output[0].split()
            return Measurement(float(measure_info[0]), measure_info[1])
    else:
        return None
    
if __name__ == "__main__": 
    POST_PROCESSED_RECIPES = []

    # For every file in the directory that contains the raw recipe data
    for recipe_filename in os.listdir(RECIPE_DIRECTORY):
        # Print the text file name for debugging
        print(recipe_filename)
        # Then take the contents of that file
        recipe_file_text = open(os.path.join(os.getcwd(), "nytimes", recipe_filename), "r").read()
        
        #### PARSE FOR NAME -- string ####
        
        #  -- Extract from XML
        recipe_name = parse_markup(recipe_file_text, XPATH_RECIPE_NAME)
        
        #  -- Then clean the data
        recipe_name = recipe_name[0].strip()
        print(recipe_name)
        
        
        #### PARSE FOR AUTHOR  -- string ####
        
        #  -- Extract from XML
        recipe_author = parse_markup(recipe_file_text, XPATH_RECIPE_AUTHOR)
        
        #  -- Then clean the data
        recipe_author = None
        if recipe_author:
            recipe_author = recipe_author[0]
            
        #print(recipe_author)
        
        
        #### PARSE FOR RECIPE YIELD  -- Measurement ####
        
        #  -- Extract from XML
        recipe_yield_list = parse_markup(recipe_file_text, XPATH_RECIPE_YIELD)
        
        #  -- Then clean the data
        recipe_yield = None
        if recipe_yield_list:
            recipe_yield_str = recipe_yield_list[0]
            
            # Remove the text about if it precedes the yield statement
            if recipe_yield_str.startswith("about "):
                recipe_yield_str = recipe_yield_str[len("about "):]
            
            # reg_qty -> "Regex for Quantities":
            # Matches zero or more digits and one or more fractional characters, possibly separated by a space
            # THIS DOES NOT MATCH CUSTOM FRACTIONS OUTSIDE THE CHARACTER SET
            reg_qty = r"(([\d\s/]+ ?[⅞⅝⅜⅛⅚⅙⅘⅗⅖⅕⅔⅓⅒⅑⅐¾½¼↉]?)|([⅞⅝⅜⅛⅚⅙⅘⅗⅖⅕⅔⅓⅒⅑⅐¾½¼↉]))"  # Outer group is 1, inner are 2 and 3
            # Tests for the reg_qty matches
            assert(re.match(reg_qty, "0").group(0) == "0")
            assert(re.match(reg_qty, "1").group(0) == "1")
            assert(re.match(reg_qty, "2").group(0) == "2")
            assert(re.match(reg_qty, "50").group(0) == "50") 
            assert(re.match(reg_qty, "⅔").group(0) == "⅔")
            assert(re.match(reg_qty, "2⅚").group(0) == "2⅚")
            assert(re.match(reg_qty, "2 ⅚").group(0) == "2 ⅚")
            assert(re.match(reg_qty, "2/3").group(0) == "2/3")
            assert(re.match(reg_qty, "5 1/2").group(0) == "5 1/2")
            # reg_unit -> "Regex for units":
            # Matches any combination of words, spaces, dashes, parentheses, and apostrophes (hors d'oeurves)
            reg_unit = r"(['\(\)\-\w\s]+)"
            # Tests for the reg_unit matches
            assert(re.match(reg_unit, "cups").group(0) == "cups")
            assert(re.match(reg_unit, "dozen brownies").group(0) == "dozen brownies")
            assert(re.match(reg_unit, "hors d'oeurves").group(0) == "hors d'oeurves")
            assert(re.match(reg_unit, "(9-inch) focaccia").group(0) == "(9-inch) focaccia")
            
            regex_yield_options = [r"serving " + reg_qty + " to " + reg_qty,
                                   r"Serves " + reg_qty + " to " + reg_qty,
                                   r"Serves " + reg_qty,
                                   reg_qty + " to " + reg_qty + "( [\-\w]*)* servings",
                                   reg_qty + "( [\-\w]*)* servings?",
                                   reg_qty + " to " + reg_qty + " " + reg_unit,
                                   reg_qty + " - " + reg_qty + " " + reg_unit,
                                   "About " + reg_qty + " " + reg_unit,
                                   "about " + reg_qty + " " + reg_unit,
                                   reg_qty + " " + reg_unit]
            for pattern in regex_yield_options:
                match = re.search(pattern, recipe_yield_str)
                if match:
                    servings_with_two_qtys = (pattern == regex_yield_options[0] or 
                                              pattern == regex_yield_options[1] or
                                              pattern == regex_yield_options[3])
                    servings_with_one_qty = (pattern == regex_yield_options[2] or 
                                             pattern == regex_yield_options[4])
                    other_unit_with_two_qtys = (pattern == regex_yield_options[5] or
                                                pattern == regex_yield_options[6])
                    other_unit_with_one_qty = (pattern == regex_yield_options[7] or
                                               pattern == regex_yield_options[8] or 
                                               pattern == regex_yield_options[9])
                    if servings_with_two_qtys:
                        # print("MATCHED SERVINGS WITH TWO QTYS: {} -> {}".format(pattern, recipe_yield_str))
                        yield_qty = max(handle_fractions(match.group(1)), handle_fractions(match.group(4)))
                        yield_units = "servings"
                    elif servings_with_one_qty:
                        # print("MATCHED SERVING WITH ONE QTY: {} -> {}".format(pattern, recipe_yield_str))
                        yield_qty = handle_fractions(match.group(1))
                        yield_units = "servings"
                    elif other_unit_with_two_qtys:
                        # print("MATCHED TWO QTYs AND A UNIT: {} -> ".format(pattern) + recipe_yield_str)
                        yield_qty = max(handle_fractions(match.group(1)), handle_fractions(match.group(4)))
                        yield_units = match.group(7)
                    elif other_unit_with_one_qty:
                        # print("MATCHED A QTY AND A UNIT: {} -> ".format(pattern) + recipe_yield_str)
                        yield_qty = handle_fractions(match.group(1))
                        yield_units = match.group(4)
                    else:
                        raise Exception("Yield data matched a regex but I don't know which one!")
                    recipe_yield = Measurement(yield_qty, yield_units)
                    break;
                        
                else:
                    continue
            
            if not recipe_yield:
                recipe_yield = recipe_yield_str
        
        
        #### PARSE FOR COOKING TIME  -- Measurement ####
        
        #  -- Extract from XML
        recipe_cooking_time_list = parse_markup(recipe_file_text, XPATH_RECIPE_COOKING_TIME)
        
        #  -- Then clean the data
        recipe_cooking_time = None
        if recipe_cooking_time_list:
            recipe_cooking_time_str = recipe_cooking_time_list[0]
            regex_cooktime = r"PT(\d*H)?(\d*M)?"
            match = re.match(regex_cooktime, recipe_cooking_time_str)
            if match:
                hours = match.group(1)
                if hours:
                    hours = int(hours.strip("H"))
                else:
                    hours = 0
                minutes = match.group(2)
                if minutes:
                    minutes = int(minutes.strip("M"))
                else:
                    minutes = 0
                recipe_cooking_time = Measurement((60*hours)+minutes, "minutes")
            else:
                recipe_cooking_time = recipe_cooking_time_str
        #print(recipe_cooking_time)
        
        
        #### PARSE FOR INGREDIENTS ####
        
        #  -- Extract from XML
        recipe_ingredients_html = parse_markup(recipe_file_text, XPATH_RECIPE_INGREDIENTS)
        
        #  -- Then clean the data
        recipe_ingredients = []
        # Convert from raw HTML to the different parts of an Ingredient
        for item in recipe_ingredients_html:
        
            # Break it up into different parts
            quantity = parse_markup(item, XPATH_INGREDIENT_QUANTITY)
            before_text = parse_markup(item, XPATH_INGREDIENT_PRE_DESC)
            core_food_item = parse_markup(item, XPATH_INGREDIENT_CORE_ELEMENT)
            after_text = parse_markup(item, XPATH_INGREDIENT_POST_DESC)
            # Then store those parts in a text string to be parsed in detail later
            ingredient_text = ""
            if quantity:
                ingredient_text += quantity[0].strip()
            if before_text:
                ingredient_text += " " + before_text[0].strip()
            if core_food_item:
                ingredient_text += " " + core_food_item[0].strip()
            if after_text:
                ingredient_text += " " + after_text[0].strip()
            # Then store the object in a list
            recipe_ingredients.append(ingredient_text)
        #pprint.pprint(recipe_ingredients)
            
        
        # PARSE FOR THE NUTRITION INFORMATION
        calories = NutritionFact(make_nutrition(parse_markup(recipe_file_text, XPATH_CALORIES), calories=True),
                                 None)
        total_fat = NutritionFact(make_nutrition(parse_markup(recipe_file_text, XPATH_FAT_CONTENT)),
                                  "total fat")
        saturated_fat = NutritionFact(make_nutrition(parse_markup(recipe_file_text, XPATH_SATURATED_FAT_CONTENT)),
                                      "saturated fat")
        trans_fat = NutritionFact(make_nutrition(parse_markup(recipe_file_text, XPATH_TRANS_FAT_CONTENT)),
                                  "trans fat")
        carbs = NutritionFact(make_nutrition(parse_markup(recipe_file_text, XPATH_CARBOHYDRATE_CONTENT)),
                              "carbohydrates")
        fiber = NutritionFact(make_nutrition(parse_markup(recipe_file_text, XPATH_FIBER_CONTENT)),
                              "fiber")
        protein = NutritionFact(make_nutrition(parse_markup(recipe_file_text, XPATH_PROTEIN_CONTENT)),
                                "protein")
        cholesterol = NutritionFact(make_nutrition(parse_markup(recipe_file_text, XPATH_CHOLESTEROL_CONTENT)),
                                    "cholesterol")
        sodium = NutritionFact(make_nutrition(parse_markup(recipe_file_text, XPATH_SODIUM_CONTENT)),
                               "sodium")

        #print(calories, total_fat, saturated_fat, trans_fat, carbs, fiber, protein, cholesterol, sodium, sep="\n")
        recipe_nutrition_information = RecipeNutrition(calories, total_fat, saturated_fat, trans_fat, 
                                                       carbs, fiber, protein, cholesterol, sodium)
        
        # PARSE FOR THE DIRECTIONS
        directions_unsplit = parse_markup(recipe_file_text, XPATH_RECIPE_DIRECTIONS)
        directions = []
        for step in directions_unsplit:
            directions += step.split(".")
        directions = [x.strip().replace('\n', '') for x in directions]
        recipe_directions = [x for x in directions if x != '']

        # Then syntesize all that data into a single structure
        recipe_obj = Recipe(recipe_name, recipe_filename, recipe_author, recipe_yield, recipe_cooking_time, 
                            recipe_ingredients, recipe_nutrition_information, recipe_directions, recipe_file_text)
        #print(recipe_obj.as_dict())
        print("Writing {} to MongoDB...".format(recipe_obj.name))
        recipe_obj.writeToMongoDB(client_mongo)
        
