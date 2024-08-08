class FoodItem:
    def __init__(self, name, protein_per_100g, fat_per_100g, carbs_per_100g,
                 calories_per_100g, category):
        self.name = name
        self.protein_per_100g = protein_per_100g
        self.fat_per_100g = fat_per_100g
        self.carbs_per_100g = carbs_per_100g
        self.calories_per_100g = calories_per_100g


def calculate_tdee_and_macros_and_generate_diet_chart(gender, weight, height, age,
                                                      activity_level, goal, food_pref):
    """
    Calculate daily calorie requirements and macronutrient needs, generate diet chart, and print it.

    Parameters:
    - gender (str): 'male' or 'female'
    - weight (float): Weight in kilograms
    - height (float): Height in centimeters
    - age (int): Age in years
    - activity_level (str): One of 'sedentary', 'light', 'moderate', 'active', 'very active'
    - goal (str): One of 'maintain', 'loss', 'gain'
    - food_pref (str): 'veg' or 'non-veg'
    """

    # Calculate BMR using Mifflin-St Jeor Equation
    if gender == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    # Adjust BMR based on activity level to get TDEE
    activity_multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very active': 1.9
    }

    if activity_level not in activity_multipliers:
        raise ValueError("Invalid activity level")

    tdee = bmr * activity_multipliers[activity_level]

    # Adjust calories based on goal
    if goal == 'maintain':
        daily_calories = tdee
    elif goal == 'loss':
        daily_calories = tdee - 500  # Roughly 0.5 kg weight loss per week
    elif goal == 'gain':
        daily_calories = tdee + 500  # Roughly 0.5 kg weight gain per week
    else:
        raise ValueError("Invalid goal")

    # Calculate macronutrient needs
    protein_calories = daily_calories * 0.30
    fat_calories = daily_calories * 0.20
    carb_calories = daily_calories * 0.50

    # Convert calories to grams
    protein_grams = protein_calories / 4  # 4 calories per gram of protein
    fat_grams = fat_calories / 9  # 9 calories per gram of fat
    carb_grams = carb_calories / 4  # 4 calories per gram of carbohydrate

    macros = {
        'protein_grams': round(protein_grams),
        'fat_grams': round(fat_grams),
        'carb_grams': round(carb_grams)
    }

    # Food databases
    food_database_nv = [
        FoodItem("Chicken Breast", 31, 3.6, 0, 165, 'P'),
        FoodItem("Rice", 2.6, 0.9, 23, 130, 'C'),
        FoodItem("Egg Whites", 11, 0, 0.2, 52, 'P'),
        FoodItem("Greek Yogurt", 10, 0.4, 17, 97, 'P'),
        FoodItem("Soya Chunks", 26, 0.5, 9, 147, 'P'),
        FoodItem("Cheese", 7, 9, 1, 113, 'P'),
        FoodItem("Chapathi", 3, 1, 18, 80, 'C'),
        FoodItem("Vegetables", 2, 0.2, 7, 34, 'V'),
        FoodItem("Whey Protein", 25, 1, 3, 130, 'P'),
        FoodItem("Fruits", 1, 0.5, 25, 60, 'F'),
    ]

    food_database_v = [
        FoodItem("Cottage Cheese", 11.1, 4.3, 3.4, 98, 'P'),
        FoodItem("Rice", 2.6, 0.9, 23, 130, 'C'),
        FoodItem("Tofu", 8, 4.8, 1.9, 76, 'P'),
        FoodItem("Greek Yogurt", 10, 0.4, 17, 97, 'P'),
        FoodItem("Soya Chunks", 26, 0.5, 9, 147, 'P'),
        FoodItem("Cheese", 7, 9, 1, 113, 'P'),
        FoodItem("Chapathi", 3, 1, 18, 80, 'C'),
        FoodItem("Vegetables", 2, 0.2, 7, 34, 'V'),
        FoodItem("Whey Protein", 25, 1, 3, 130, 'P'),
        FoodItem("Fruits", 1, 0.5, 25, 60, 'F'),
    ]

    user_requirements = {
        "protein": macros['protein_grams'],
        "fat": macros['fat_grams'],
        "carbs": macros['carb_grams'],
        "calories": daily_calories
    }

    if food_pref == "veg":
        food_database = food_database_v
    else:
        food_database = food_database_nv

    # Generate diet chart
    diet_chart = generate_diet_chart(user_requirements, food_database)

    # Print diet chart as a table
    # print_diet_chart(diet_chart)

    return round(daily_calories), macros, diet_chart


def calculate_food_amount(nutrient_goal, nutrient_per_100g):
    return (nutrient_goal / nutrient_per_100g) * 100


def generate_diet_chart(user_requirements, food_database):
    meal_ratios = {
        "breakfast": 0.15,
        "lunch": 0.35,
        "snacks": 0.25,
        "dinner": 0.25
    }
    diet_chart = {meal: [] for meal in ["breakfast", "lunch", "snacks", "dinner"]}

    for meal in diet_chart:
        meal_calories = user_requirements["calories"] * meal_ratios[meal]
        meal_protein = user_requirements["protein"] * meal_ratios[meal]
        meal_fat = user_requirements["fat"] * meal_ratios[meal]
        meal_carbs = user_requirements["carbs"] * meal_ratios[meal]

        total_calories = 0
        total_protein = 0
        total_fat = 0
        total_carbs = 0

        if meal in ["lunch", "dinner"]:
            for food_item in food_database:
                if food_item.name == "Vegetables":
                    diet_chart[meal].append({"food": "Vegetables", "amount": 100})
                    total_calories += (food_item.calories_per_100g / 100) * 100
                    total_protein += (food_item.protein_per_100g / 100) * 100
                    total_fat += (food_item.fat_per_100g / 100) * 100
                    total_carbs += (food_item.carbs_per_100g / 100) * 100
                    break

        for food_item in food_database:
            if meal in ["breakfast", "snacks"] and food_item.name == "Rice":
                continue
            if meal == "breakfast" and food_item.name == "Chicken Breast":
                continue

            if total_calories >= meal_calories and total_protein >= meal_protein:
                break

            amount = calculate_food_amount(meal_protein, food_item.protein_per_100g)
            calories = (food_item.calories_per_100g / 100) * amount
            if total_calories + calories > meal_calories:
                amount = ((
                                  meal_calories - total_calories) / food_item.calories_per_100g) * 100
                calories = meal_calories - total_calories

            diet_chart[meal].append({"food": food_item.name, "amount": round(amount, 2)})
            total_calories += calories
            total_protein += (food_item.protein_per_100g / 100) * amount
            total_fat += (food_item.fat_per_100g / 100) * amount
            total_carbs += (food_item.carbs_per_100g / 100) * amount

    return diet_chart


def print_diet_chart(diet_chart):
    # Define the header
    header = f"{'Meal':<15}{'Food':<25}{'Amount (g)':<10}"
    print(header)
    print('-' * len(header))

    # Print each meal and its items
    for meal, items in diet_chart.items():
        first_row = True
        for item in items:
            meal_name = meal.capitalize() if first_row else ""
            row = f"{meal_name:<15}{item['food']:<25}{item['amount']:<10.2f}"
            print(row)
            first_row = False


def format_diet_chart_html(diet_chart):
    # Start the HTML string
    message = """
        <p>This diet chart is based on your height, weight, age, and eating preferences.</p>
        <table class='table'>
            <tr>
                <th>Meal</th>
                <th>Food</th>
                <th>Amount (g)</th>
            </tr>
    """

    # Define the HTML rows
    for meal, items in diet_chart.items():
        first_row = True
        for item in items:
            meal_name = meal.capitalize() if first_row else ""
            row = f"""
            <tr>
                <td>{meal_name}</td>
                <td>{item['food']}</td>
                <td>{item['amount']:.2f}</td>
            </tr>
    """
            message += row
            first_row = False

    # End the HTML string
    message += """
        </table>
    """
    return message


if __name__ == "__main__":
    # Example usage
    gender = 'female'
    weight = 70  # in kg
    height = 170  # in cm
    age = 27
    activity_level = 'moderate'
    goal = 'loss'
    food_pref = 'nonVeg'

    daily_calories, macros, diet_chart = calculate_tdee_and_macros_and_generate_diet_chart(
        gender, weight, height, age, activity_level, goal, food_pref)

    print(f"Daily Calorie that you need to take: {daily_calories} calories")
