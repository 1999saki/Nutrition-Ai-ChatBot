import csv
import json

import requests
from bs4 import BeautifulSoup

all_recipes = dict()


def main_scrapping_start():
    with open("recipe_list.csv", "r") as c_recipe:
        c = csv.reader(c_recipe)
        for row in c:
            recipe = dict()

            recipe_name = row[1]
            print(recipe_name)

            recipe_site = row[0]

            try:
                con = requests.get(recipe_site, headers={'User-Agent': 'Magic-Browser'})
                html = BeautifulSoup(con.content, 'html.parser')

                ingredients = html.findAll('li', attrs={'class': 'ingredient',
                                                        'itemprop': 'ingredients'})
                instructions = html.findAll('li', attrs={'class': 'instruction',
                                                         'itemprop': 'recipeInstructions'})
                servings = html.find('span', attrs={'itemprop': 'recipeYield'})
                prep_time = html.find('time', attrs={'itemprop': 'prepTime'})
                cook_time = html.find('time', attrs={'itemprop': 'cookTime'})
                total_time = html.find('time', attrs={'itemprop': 'totalTime'})

                try:
                    recipe['prep_time'] = prep_time.contents[0]
                except:
                    recipe['prep_time'] = ""

                try:
                    recipe['cook_time'] = cook_time.contents[0]
                except:
                    recipe['cook_time'] = ""

                try:
                    recipe['total_time'] = total_time.contents[0]
                except:
                    recipe['total_time'] = ""

                ingre_list = list()
                instr_list = list()

                for ingre in ingredients:
                    ingre_list.append(ingre.contents[0])

                for instr in instructions:
                    instr_list.append(instr.contents[0])

                recipe['ingredients'] = ingre_list
                recipe['instructions'] = instr_list

                all_recipes[recipe_name] = recipe

            except:
                print("can't connect")

    try:
        with open('recipes.json', 'w') as jfile:
            json.dump(all_recipes, jfile, sort_keys=True, indent=4)
    except:
        import pprint
        pprint.pprint(all_recipes)


api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
total_ingredients = ['Allspice', 'Club soda', 'Salt', 'Coffee', 'Celery', 'Rhubarb',
                     'Lemon juice', 'Cucumber', 'Chicory', 'Fennel', 'Radish', 'Endive',
                     'Mushrooms', 'Mustard and cress', 'Pumpkin', 'Lettuce',
                     'Raddiccio', 'Eggplant', 'Vine leaves', 'Cranberries',
                     'Canned tomatoes', 'Tomatoes', 'Artichoke', 'Celeriac',
                     'Cherry tomatoes', 'Swiss chard', 'Gooseberries', 'Canteloupe',
                     'Pepper', 'Shallots', 'Coriander leaves',
                     'Pickle, mixed vegetables', 'Leeks', 'Watercress', 'Coconut milk',
                     'Vinegar', 'Balor beans', 'Spring onions', 'Turnip', 'Chives',
                     'Green beans', 'Alfalfa sprouts', 'Swede', 'Melon', 'Galia',
                     'Asparagus', 'Spinach', 'Blackberries', 'Raspberries', 'Dill',
                     'Cabbage', 'Hot pepper sauce', 'Mustard leaves', 'Papaya',
                     'Strawberries', 'Honeydew', 'Tamarillos', 'Carrots', 'Beansprouts',
                     'Okra', 'Watermelon', 'Skim milk', 'Mandarin oranges', 'Broccoli',
                     'Radish leaves', 'Spring greens', 'Orange juice', 'Tonic water',
                     'Grapefruit juice', 'Sugar-snap peas', 'Cauliflower', 'Apricots',
                     'Parsley', 'Fenugreek leaves', 'Tangerines', 'Beetroot', 'Onions',
                     'Butternut squash', 'Passion fruit', 'Plums', 'Orange juice',
                     'Buttermilk', 'Clementines', 'Oranges', 'Apple juice',
                     'Acorn squash', 'Nectarines', 'Pears', 'Basil', 'Pineapple',
                     'Pineapple juice', 'Brussels sprouts', 'Seaweed', 'Figs',
                     'Mint, fresh', 'Soy sauce', 'Sweet and sour sauce',
                     'Water chestnuts', 'Grape juice', 'Apples', 'Pasta sauce, tomato',
                     'Cherries', 'Kiwi fruit', 'Ginger', 'Tarragon', 'Lotus tubers',
                     'Pomegranate', 'Sweetcorn', 'Mango', 'Grapes', 'Betel leaves',
                     'Cranberry juice', 'Horseradish', 'Parsnip',
                     'Worcestershire sauce', 'Whole milk', 'Oregano', 'Tofu', 'Potato',
                     'Coffee', 'Tzatziki', 'Tomato puree', 'Curry sauce',
                     'Chilli sauce', 'Peas', 'Sweet potato', 'Bananas', 'Thyme',
                     'Curry leaves', 'Garlic', 'Rosemary', 'Cottage cheese', 'Olives',
                     'Venison', 'Pork shoulder', 'Turkey, meat only', 'Taro',
                     'Veal, escalope', 'Chicken, light meat', 'Arrowhead', 'Ham',
                     'Chicken, meat only', 'Yogurt', 'Chicken, dark meat', 'Yam',
                     'Relish, burger/chilli/tomato', 'Tamarind leaves',
                     'Tomato ketchup', 'Plantain', 'Sage',
                     'Relish, corn/cucumber/onion', 'Pastrami', 'Dates', 'Guacamole',
                     'Chutney, tomato', 'Ham, premium', 'Pasta sauce, white',
                     'Whole turkey', 'Greek yogurt', 'Duck, meat only',
                     'Rabbit, meat only', 'Beef slices', 'Mustard', 'Pickle', 'Cassava',
                     'Veal, mince', 'Beef, stewing steak', 'Pork, diced',
                     'Pork, fillet', 'Evaporated milk', 'Egg', 'Pork, chump steaks',
                     'Cranberry sauce', 'Horseradish sauce', 'Beef, fillet steak',
                     'Chutney, mixed fruit', 'Mushroom', 'Prunes',
                     'Beef, braising steak', 'Baking powder', 'Pork, mince',
                     'Turkey roll', 'Pork, spare rib steaks', 'Pork, steaks',
                     'Chestnuts', 'Beef, rump steak', 'Yeast', 'Pork, spare rib chops',
                     'Hummus', 'Lamb, leg', 'Chutney, mango', 'Avocado',
                     'Chicken, leg quarter', 'Chicken, wing quarter',
                     'Pork, chump chops', 'Pork, spare ribs', 'Lamb, mince',
                     'Beef, topside', 'Beef, sirloin steak', 'Whole chicken', 'Miso',
                     'Lamb, stewing', 'Corned beef', 'Bran', 'Brown bread', 'Spinach',
                     'Pork, leg joint', 'Beef, silverside', 'Whole bread',
                     'Beef, brisket', 'Pork, hand, shoulder joint',
                     'Pork, spare rib joint', 'Rye bread', 'Peaches',
                     'Lamb, chump steaks', 'Ham, Parma', 'Beef, mince',
                     'Pork, loin steaks', 'Lamb, neck fillet', 'Curry powder',
                     'White bread', 'Lamb, shoulder', 'Cream', 'Curry paste', 'Chervil',
                     'Stock cubes, chicken', 'Tamarind', 'Lamb, chump chops',
                     'Garlic powder', 'Pork, loin joint', 'Cheese, Feta',
                     'Stock cubes, vegetable', 'Pita bread', 'Cheese, Mozzarella',
                     'Pork, belly joint/slices', 'Bratwurst', 'Marmalade',
                     'Syrup, maple', 'Hamburger buns', 'Ham and pork',
                     'Red kidney beans', 'Beef, flank', 'Molasses', 'Cheese spread',
                     'Pork, loin chops', 'Pickle, chilli', 'Raisins', 'Tamarind pulp',
                     'Pasta', 'Sultanas', 'Pork and beef sausages', 'Lamb, loin chops',
                     'Mung beans', 'Luncheon meat', 'Honeycomb', 'Syrup, corn',
                     'Rack of lamb', 'Mushrooms, Chinese', 'Naan bread',
                     'Chutney, mango', 'Lamb, breast', 'Honey', 'Paprika',
                     'Butter beans', 'Beef sausages', 'Chorizo', 'Mushrooms, shiitake',
                     'Syrup, golden', 'Tartare sauce', 'Barley', 'Lamb, loin joint',
                     'Quinoa', 'Pork sausages', 'Saffron', 'Blackeyed peas',
                     'Cocoa powder', 'Bay leaf', 'Lentils', 'Pepper, cayenne',
                     'Chick peas', 'Dressing, thousand island', 'Pinto beans',
                     'Potato flour', 'Turkey, skin', 'Condensed milk', 'Gelatine',
                     'Pork and beef sausages', 'Wheat flour', 'Sweetcorn',
                     'Cheese, brie', 'Macaroni', 'Coconut cream', 'Coconut',
                     'Cornflour', 'Custard powder', 'Red rice', 'Breadcrumbs',
                     'Vermicelli', 'Brown rice', 'Rice noodles', 'White rice', 'Goose',
                     'Sugar, brown', 'Buckwheat', 'Rice flour', 'Cornmeal',
                     'Soya beans', 'Croissants', 'Puff pastry', 'Cheese, Gouda',
                     'Creme fraiche', 'Garam masala', 'Cheese, white', 'Plain noodles',
                     'Duck, meat fat skin', 'Egg noodles', 'Sugar, white', 'Oatmeal',
                     'Gruyere cheese', 'Cheddar cheese', 'Parmesan cheese', 'Salami',
                     'Cream cheese', 'Mustard powder', 'Dressing, blue cheese',
                     'Dressing, French', 'Chicken, skin', 'Banana chips', 'Chocolate',
                     'Peanuts', 'Pumpkin seeds', 'Cashew nuts', 'Sunflower seeds',
                     'Melon seeds', 'Sesame seeds', 'Peanut butter', 'Tahini paste',
                     'Almonds', 'Hazelnuts', 'Dressing, oil and lemon', 'Brazil nuts',
                     'Pine nuts', 'Walnuts', 'Pecan nuts', 'Margarine', 'Butter',
                     'Bacon', 'Macadamia nuts', 'Suet', 'Cottonseed oil',
                     'Dripping, beef', 'Lard', 'Sesame oil', 'Coconut oil', 'Corn oil',
                     'Grapeseed oil', 'Hazelnut oil', 'Olive oil', 'Palm oil',
                     'Safflower oil', 'Sunflower oil', 'Vegetable oil', 'Walnut oil',
                     'Caraway seeds', 'Cardamom', 'Celery seeds', 'Chilli powder',
                     'Chinese 5 spice', 'Cinnamon', 'Cloves', 'Cumin seeds', 'Tea', ]

master_ingredient_dict = {
    'spices': ['paprika', 'cayenne pepper', 'chili powder', 'curry powder',
               'vanilla extract', 'vanilla bean', 'kosher salt', 'bay leaf',
               'bay leaves', 'crushed red pepper', 'ginger', 'baking powder',
               'baking soda', 'cinnamon', 'saffron', 'mint', 'tarragon', 'chives',
               'fennel', 'parsley', 'sage', 'allspice', 'dill', 'marjoram', 'cumin',
               'oregano', 'thyme', 'rosemary', 'basil', 'tumeric', 'cardamom', 'nutmeg',
               'clove', 'star anise', 'anise', 'basil', 'smoked paprika',
               'garlic powder', 'onion powder', 'almond extract', 'coriander', 'salt',
               'garlic salt', 'celery salt', 'black pepper', 'peppercorns',
               'white pepper', 'five spice', '5-spice', 'five spice powder',
               '5-spice powder', 'cilantro', 'old bay', 'mustard powder',
               'pepper flakes', 'sesame seeds'],
    'others': ['worcestershire sauce', 'soy sauce', 'cocoa powder', 'chocolate chip',
               'light soy sauce', 'dark soy sauce', 'hoisin sauce', 'corn starch',
               'water', 'capers', 'granulated sugar', 'sugar', 'brown sugar',
               'molasses', "confectioner's sugar", 'lemon juice', 'lime juice',
               'lemon zest', 'lime zest', 'zest', 'v-8 juice', 'white wine', 'red wine',
               'red wine vinegar', 'white wine vinegar', 'white vinegar',
               'vegetable stock', 'beef stock', 'chicken stock', 'fish sauce',
               'whole grain mustard', 'mustard', 'ketchup', 'dijon mustard', 'honey',
               'agave', 'mayonnaise', 'beer', 'whiskey', 'cognac', 'teriyaki sauce',
               'brandy', 'vodka', 'espresso', 'sherry'],
    'oils': ['sunflower oil', 'peanut oil', 'palm oil', 'cottonseed oil', 'olive oil',
             'extra virgin olive oil', 'coconut oil', 'canola oil',
             'corn oil''sesame oil', 'soybean oil', 'vegetable oil', 'rapeseed oil',
             'lard', 'vegetable shortening', 'shortening', 'suet', 'fat'],
    'milk': ['salted butter', 'unsalted butter', 'butter', 'margarine', 'buttermilk',
             'condensed milk''custard', 'dulce de leche', 'evaporated milk',
             'frozen yogurt', 'whole milk', 'skim milk', 'reduced fat milk', 'whey'],
    'cream': ['sour cream', 'clotted cream', 'cream', 'heavy cream', 'whipped cream',
              'creme fraiche', 'ice cream'],
    'yogurt': ['yogurt', 'greek yogurt', 'plain yogurt'],
    'cheese': ['cheddar cheese', 'cream cheese', 'goat cheese', 'feta', 'brie',
               'ricotta cheese', 'jalapeno jack', 'cream cheese', 'cottage cheese',
               'mozzarella', 'parmigiano-reggiano', 'blue cheese', 'gouda cheese',
               'american cheese', 'camembert', 'roquefort', 'provolone',
               'gruyere cheese', 'monterey jack', 'stilton cheese', 'gorgonzola',
               'emmental cheese', 'ricotta', 'swiss cheese', 'colby cheese',
               'parmesan cheese', 'muenster cheese', 'pecorino', 'manchego', 'edam',
               'halloumi', 'havarti', 'pecorino romano', 'comte cheese', 'grana',
               'asiago cheese''pepper jack cheese''mascarpone', 'limburger',
               'American Cheese', 'processed cheese'],
    'potatoes': ['potato', 'sweet potato', 'taro', 'yam''idaho potato', 'russet potato',
                 'yukon gold', 'fingerlings'],
    'rice': ['brown rice', 'white rice', 'basmati', 'wild rice', 'jasmine rice',
             'glutinous rice'],
    'breads': ['barley', 'millet', 'buckwheat', 'corn', 'oats', 'steel-cut oats',
               'rolled oats', 'instant oats', 'quinoa', 'rye', 'granola',
               'all-purpose flour', 'semolina', 'whole-wheat flour', 'enriched flour',
               'cake flour', 'self-rising flour', 'sourdough', 'white bread',
               'rye bread', 'pita', 'baguette', 'focaccia', 'naan', 'banana bread',
               'bagel', 'pumpernickel', 'challah', 'croissant', 'english muffin',
               'raisin bread', 'garlic bread', 'biscuit', 'bun', 'hot dog bun',
               'hamburger bun'],
    'pastas': ['angel hair', 'linguine', 'fettuccine', 'orecchiette', 'orzo',
               'rigatoni', 'spaghetti', 'gnocchi', 'fusilli', 'farfalle',
               'penne''tortellini', 'rotelle', 'lasagne', 'vermicelli', 'ramen', 'soba',
               'udon', 'rice vermicelli', 'noodle'],
    'shrooms': ['shittake', 'morel', 'enokitake', 'oyster mushroom', 'white mushroom',
                'white button', 'portobello'],
    'fruits': ["apple", "pineapple", "grapefruit", "banana", "orange", 'blueberry',
               "strawberry", "grape", 'raisin', 'cranberry', "lemon", "cherry", "pear",
               "mango", "avocado", "peach", "melon", "apricot", "plum", "kiwi",
               'watermelon', 'blackberry', 'papaya', 'cantaloupe', 'berry', 'tangerine',
               'coconut', 'cranberry', 'lychee', 'date', 'passion fruit''gooseberry',
               'persimmon', 'lime', "nectarine", "fig", "pomegranate"],
    'greens': ['spinach', 'kale', 'cabbage', 'broccoli', 'dandelion', 'leafy green',
               'chard', 'lettuce', 'rapini', 'endive', 'napa cabbage', 'cauliflower',
               'tomato', 'squash', 'cucumber', 'bell pepper', 'pumpkin', 'corn',
               'maize', 'brussel sprout', 'artichoke', 'bell pepper', 'chili pepper',
               'red pepper', 'arugula', 'watercress''butternut squash',
               'eggplant''diced tomato', 'crushed tomato', 'tomato paste', 'jalapeno',
               'radish', 'bok choy'],
    'legumes': ['bean', 'soybean', 'nut', 'lentil', 'pea', 'okra', 'green bean',
                'kidney bean', 'navy bean', 'pinto bean', 'garbanzo bean', 'wax bean',
                'mung bean', 'snow pea', 'lima pea''alfalfa', 'clover', 'snap pea',
                'sugar snap pea', 'snow pea', 'peanut butter', 'almond butter',
                'cashew butter', 'peanut', 'almond', 'walnut', 'cashew', 'pecan',
                'pistachio', 'hazelnut', 'brazil nut', 'pine nut', 'macadamia',
                'chestnut'],
    'roots': ['carrot', 'parsnip', 'turnip', 'rutabaga', 'radish', 'celery', 'daikon',
              'kohirabi', 'scalllion', 'jicama', 'horseradish', 'onion', 'shallot',
              'vidalia onion', 'red onion', 'pearl onion', 'leek', 'water chestnut',
              'spring onion', 'yellow onion', 'white onion', 'asparagus', 'chicory',
              'garlic'],
    'eggs': ['egg', 'chicken egg', 'duck egg', 'goose egg', 'quail egg'],
    'lamb': ['lamb', 'lamb chop', 'lamb loin chop', 'lamb rack', 'rack of lamb',
             'lamb rib', 'ground lamb', 'lamb shank', 'lamb sirloin',
             'boneless lamb leg', 'bone-in lamb leg'],
    'pork': ['pork', 'pork shoulder', 'pork butt', 'pork loin', 'pork chop',
             'loin chop', 'sirloin chop', 'sirloin steak', 'baby back rib', 'riblet',
             'rack of pork', 'pork loin half rib', 'pork tenderloin', 'sirloin roast',
             'spare rib', 'pork sausage', 'ground pork', 'bacon', 'ham'],
    'beef': ['beef', 't-bone steak', 'strip steak', 'chuck steak', 'skirt steak',
             'brisket', 'flank steak', 'short loin', 'flat iron steak', 'short ribs',
             'rib eye steak', 'rib steak', 'round steak', 'sirloin steak',
             'top sirloin', 'bottom sirloin', 'hanger steak', 'beef tenderloin',
             'ground beef', 'beef sausage'],
    'chicken': ['chicken', 'chicken breast', 'chicken wing', 'chicken drum',
                'chicken drumstick', 'chicken thigh', 'chicken leg', 'whole chicken',
                'chicken quarter']
}
result_data = []


def make_call(ing):
    response = requests.get(api_url + ing, headers={
        'X-Api-Key': 'yvU4M/XVCe1IOTph1K4qWw==dBbTSkkHpfaUouTd'})
    if response.status_code == requests.codes.ok:
        return response.json()['items']
    else:
        print("Error:", response.status_code, response.text)
        return []


def get_ingredients_info():
    for categ, data in master_ingredient_dict.items():
        for ing in data:
            res = make_call(ing)
            if res:
                res[0]['category'] = categ
            result_data.extend(res)
    return result_data


get_ingredients_info()
headers = result_data[0].keys()
with open('new_scrapped_food_data.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(result_data)

print("CSV file has been created successfully.")
