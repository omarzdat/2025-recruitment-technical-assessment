from dataclasses import dataclass
from typing import List, Dict, Union
from flask import Flask, request, jsonify
import re

# ==== Type Definitions, feel free to add or modify ===========================
@dataclass
class CookbookEntry:
    name: str
    type: str 

@dataclass
class RequiredItem:
    name: str
    quantity: int

@dataclass
class Recipe(CookbookEntry):
    required_items: List[RequiredItem]
    
    def __init__(self, name: str, required_items: List[RequiredItem]):
        super().__init__(name=name, type="recipe")
        self.required_items = required_items

@dataclass
class Ingredient(CookbookEntry):
    cook_time: int
    
    def __init__(self, name: str, cook_time: int):
        super().__init__(name=name, type="ingredient")
        self.cook_time = cook_time


# =============================================================================
# ==== HTTP Endpoint Stubs ====================================================
# =============================================================================
app = Flask(__name__)

# Store your recipes here!
cookbook = {}

# Task 1 helper (don't touch)
@app.route("/parse", methods=['POST'])
def parse():
	data = request.get_json()
	recipe_name = data.get('input', '')
	parsed_name = parse_handwriting(recipe_name)
	if parsed_name is None:
		return 'Invalid recipe name', 400
	return jsonify({'msg': parsed_name}), 200

# [TASK 1] ====================================================================
# Takes in a recipeName and returns it in a form that 
def parse_handwriting(recipeName: str) -> Union[str | None]:
	if recipeName is None:
		return None

	# Hyphens and underscores
	processed = recipeName.replace('-', ' ').replace('_', ' ')

	# Non-alphabet
	processed = ''.join(char for char in processed if char.isalpha() or char.isspace())

	# Spaces, in and leading
	processed = ' '.join(word for word in processed.split() if word)

	# Lengthcheck
	if len(processed) == 0:
		return None

	# Capitalization :3
	processed = ' '.join(word.capitalize() for word in processed.split())

	return processed

# [TASK 2] ====================================================================
# Endpoint that adds a CookbookEntry to your magical cookbook
@app.route('/entry', methods=['POST'])
def create_entry():
    data = request.get_json()
    
	# consider case where requireditem is empty?
    # should it be rejected?
    
    if not data or 'name' not in data or 'type' not in data:
        return 'Missing required fields', 400
    entry_type = data.get('type')
    if entry_type not in ['recipe', 'ingredient']:
        return 'Invalid entry type', 400
    entry_name = parse_handwriting(data.get('name'))
    if entry_name is None:
        return 'Invalid entry name', 400
    if entry_name in cookbook:
        return 'Entry name already exists', 400
    
    if entry_type == 'ingredient':
        if 'cookTime' not in data:
            return 'Missing cookTime field for ingredient', 400
        
        cook_time = data.get('cookTime')
        if not isinstance(cook_time, int) or cook_time < 0:
            return 'cookTime must be a non-negative integer', 400
        
        entry = Ingredient(name=entry_name, cook_time=cook_time)
    
    else:
        if 'requiredItems' not in data:
            return 'Missing requiredItems field for recipe', 400
        
        if not isinstance(data.get('requiredItems'), list):
            return 'requiredItems must be a list', 400
        
        required_items = []
        required_item_names = set()
        
        for item in data.get('requiredItems'):
            if 'name' not in item or 'quantity' not in item:
                return 'Required items must have name and quantity', 400
            
            item_name = parse_handwriting(item.get('name'))
            if item_name is None:
                return 'Invalid required item name', 400
            
            if item_name in required_item_names:
                return 'Duplicate required item name', 400
            
            if not isinstance(item.get('quantity'), int) or item.get('quantity') <= 0:
                return 'Quantity must be a positive integer', 400
            
            required_items.append(RequiredItem(name=item_name, quantity=item.get('quantity')))
            required_item_names.add(item_name)
        
        entry = Recipe(name=entry_name, required_items=required_items)
    
    cookbook[entry_name] = entry
    
    return '', 200


# [TASK 3] ====================================================================
# Endpoint that returns a summary of a recipe that corresponds to a query name
@app.route('/summary', methods=['GET'])
def summary():
    # Get recipe name from query parameters
    recipe_name = request.args.get('name')
    if not recipe_name:
        return 'Missing recipe name', 400
    
    # Parse and normalize the recipe name
    recipe_name = parse_handwriting(recipe_name)
    if recipe_name is None:
        return 'Invalid recipe name', 400
    
    # Check if recipe exists in cookbook
    if recipe_name not in cookbook:
        return 'Recipe not found', 400
    
    # Get the entry
    entry = cookbook[recipe_name]
    
    # Strictly check if the entry is a Recipe instance
    if not isinstance(entry, Recipe):
        return 'Entry is not a recipe', 400
    
    # Double-check type field as well
    if getattr(entry, 'type', None) != 'recipe':
        return 'Entry is not a recipe', 400
    
    # Calculate cook time and collect base ingredients recursively
    try:
        cook_time, ingredients = calculate_recipe_details(recipe_name)
        
        # Merge ingredients with the same name by summing their quantities
        merged_ingredients = {}
        for item in ingredients:
            if item.name in merged_ingredients:
                merged_ingredients[item.name] += item.quantity
            else:
                merged_ingredients[item.name] = item.quantity
        
        # Convert back to list of RequiredItem objects
        ingredient_list = [
            {"name": name, "quantity": quantity}
            for name, quantity in merged_ingredients.items()
        ]
        
        # Prepare the summary response
        summary_response = {
            "name": recipe_name,
            "cookTime": cook_time,
            "ingredients": ingredient_list
        }
        
        return jsonify(summary_response), 200
    
    except Exception as e:
        # Catch any exception, not just KeyError
        return f'Error processing recipe: {str(e)}', 400

# Recursive calculation for cook time and collec base ingredients
def calculate_recipe_details(recipe_name):
    recipe = cookbook[recipe_name]
    
    # Base case: if it's an ingredient, not a recipe
    if recipe.type == 'ingredient':
        return recipe.cook_time, []
    
    total_cook_time = 0
    all_ingredients = []
    
    # Process each required item
    for required_item in recipe.required_items:
        item_name = required_item.name
        item_quantity = required_item.quantity
        
        # Check if the required item exists in the cookbook
        if item_name not in cookbook:
            raise KeyError(f"Required item '{item_name}' not found in cookbook")
        
        item = cookbook[item_name]
        
        if item.type == 'ingredient':
            # It's a base ingredient
            total_cook_time += item.cook_time * item_quantity
            all_ingredients.append(RequiredItem(name=item_name, quantity=item_quantity))
        else:
            # It's another recipe, recursively calculate
            sub_cook_time, sub_ingredients = calculate_recipe_details(item_name)
            total_cook_time += sub_cook_time * item_quantity
            
            # Scale the quantities of sub-ingredients
            for sub_item in sub_ingredients:
                scaled_item = RequiredItem(
                    name=sub_item.name,
                    quantity=sub_item.quantity * item_quantity
                )
                all_ingredients.append(scaled_item)
    
    return total_cook_time, all_ingredients

@app.route('/reset', methods=['POST'])
def reset_cookbook():
    global cookbook
    cookbook = {}
    return '', 200

# =============================================================================
# ==== DO NOT TOUCH ===========================================================
# =============================================================================

if __name__ == '__main__':
	app.run(debug=True, port=8080)
