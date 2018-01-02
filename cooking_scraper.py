#import statements
from bs4 import BeautifulSoup
import time
import urllib2

RECIPES_URL_BASE = "https://cooking.nytimes.com/recipes/"
RECIPE_INDEX = 1010000
DELAY_SECONDS = 0.1

while RECIPE_INDEX < 1015000:
    print "Getting recipe page at index {}...".format(RECIPE_INDEX)
    try:
        page = urllib2.urlopen(RECIPES_URL_BASE + str(RECIPE_INDEX))  # Ask for the page at the current index
    except urllib2.HTTPError:
        print "HTTP Error: No recipe page at index {}".format(RECIPE_INDEX)
    else:
        try:
            soup = BeautifulSoup(page, 'html.parser')  # Convert the page into a BeautifulSoup object
            recipe_info = soup.find(attrs={"data-type": "recipe"})  # Pull the HTML that contains the recipe information
            if not recipe_info:  # If the page we got doesn't have a recipe...
                print "Huh... no recipe for the page found at index {}".format(RECIPE_INDEX)
            else:  # Otherwise we do have a recipe, so in that case...
                # Save the recipe text to the current directory as a plain HTML file
                file_name = "nytimes_recipe_{}.html".format(RECIPE_INDEX)
                with open(file_name, "w") as f:
                    f.write(str(recipe_info))
                print "Recipe #{} saved to HTML file".format(RECIPE_INDEX)
        except Exception as e:
            print "Uh-oh! Error occurred for the HTML we got at index {}: {}".format(RECIPE_INDEX, e)
    finally:
        print "Sleeping {} seconds to avoid detection by the NYTimes...".format(DELAY_SECONDS)
        time.sleep(DELAY_SECONDS)
        RECIPE_INDEX += 1
