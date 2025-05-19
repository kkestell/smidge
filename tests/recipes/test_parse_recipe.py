from src.smidge import parse_recipe


def test_form1_simple_recipe():
    recipe_text = """= Toast

- 2 slices bread
- 1 pat butter

# Toast the bread
# Spread butter on toast
# Serve hot
"""
    result = parse_recipe(recipe_text)

    assert result.title == "Toast"
    assert len(result.components) == 1

    component = result.components[0]
    assert component.name is None
    assert component.ingredients == ["2 slices bread", "1 pat butter"]
    assert len(component.steps) == 3
    assert component.steps[0].text == "Toast the bread"
    assert component.steps[1].text == "Spread butter on toast"
    assert component.steps[2].text == "Serve hot"

    for step in component.steps:
        assert step.ingredients is None


def test_form2_ingredients_by_step():
    recipe_text = """= Boiled Egg

# Boil water
  - 4 cups water
  - 1 pinch salt

# Add egg
  - 1 egg

# Cool in ice water
  - 2 cups ice water

# Peel and serve
"""
    result = parse_recipe(recipe_text)

    assert result.title == "Boiled Egg"
    assert len(result.components) == 1

    component = result.components[0]
    assert component.name is None
    assert component.ingredients is None
    assert len(component.steps) == 4

    step1 = component.steps[0]
    assert step1.text == "Boil water"
    assert step1.ingredients == ["4 cups water", "1 pinch salt"]

    step2 = component.steps[1]
    assert step2.text == "Add egg"
    assert step2.ingredients == ["1 egg"]

    step3 = component.steps[2]
    assert step3.text == "Cool in ice water"
    assert step3.ingredients == ["2 cups ice water"]

    step4 = component.steps[3]
    assert step4.text == "Peel and serve"
    assert step4.ingredients is None


def test_form3_multiple_components():
    recipe_text = """= Sandwich

+ Sauce

- 2 tbsp mayo
- 1 tsp mustard

# Mix ingredients

+ Sandwich

- 2 slices bread
- 1 slice cheese
- 1 slice ham

# Spread sauce on bread
# Add cheese and ham
# Close sandwich
"""
    result = parse_recipe(recipe_text)

    assert result.title == "Sandwich"
    assert len(result.components) == 2

    sauce = result.components[0]
    assert sauce.name == "Sauce"
    assert sauce.ingredients == ["2 tbsp mayo", "1 tsp mustard"]
    assert len(sauce.steps) == 1
    assert sauce.steps[0].text == "Mix ingredients"

    sandwich = result.components[1]
    assert sandwich.name == "Sandwich"
    assert sandwich.ingredients == ["2 slices bread", "1 slice cheese", "1 slice ham"]
    assert len(sandwich.steps) == 3
    assert sandwich.steps[0].text == "Spread sauce on bread"
    assert sandwich.steps[1].text == "Add cheese and ham"
    assert sandwich.steps[2].text == "Close sandwich"


def test_form4_components_with_step_ingredients():
    recipe_text = """= Salad

+ Dressing

# Whisk oil and vinegar
  - 2 tbsp oil
  - 1 tbsp vinegar

# Add salt and pepper
  - 1/2 tsp salt
  - 1/4 tsp pepper

+ Salad

# Chop lettuce
  - 1 head lettuce

# Toss with dressing
"""
    result = parse_recipe(recipe_text)

    assert result.title == "Salad"
    assert len(result.components) == 2

    dressing = result.components[0]
    assert dressing.name == "Dressing"
    assert dressing.ingredients is None
    assert len(dressing.steps) == 2

    assert dressing.steps[0].text == "Whisk oil and vinegar"
    assert dressing.steps[0].ingredients == ["2 tbsp oil", "1 tbsp vinegar"]

    assert dressing.steps[1].text == "Add salt and pepper"
    assert dressing.steps[1].ingredients == ["1/2 tsp salt", "1/4 tsp pepper"]

    salad = result.components[1]
    assert salad.name == "Salad"
    assert salad.ingredients is None
    assert len(salad.steps) == 2

    assert salad.steps[0].text == "Chop lettuce"
    assert salad.steps[0].ingredients == ["1 head lettuce"]

    assert salad.steps[1].text == "Toss with dressing"
    assert salad.steps[1].ingredients is None


def test_empty_recipe():
    result = parse_recipe("")
    assert result is None


def test_no_title():
    recipe_text = """
- 1 egg

# Cook egg
"""
    result = parse_recipe(recipe_text)
    assert result is None


def test_mixed_spacing():
    recipe_text = """= Pasta

- 1 cup pasta
- 2 cups water
- salt

# Boil water
# Add pasta
  - pinch of salt
# Drain
"""
    result = parse_recipe(recipe_text)

    assert result.title == "Pasta"
    assert len(result.components) == 1

    component = result.components[0]
    assert component.ingredients == ["1 cup pasta", "2 cups water", "salt"]
    assert len(component.steps) == 3

    assert component.steps[0].ingredients is None
    assert component.steps[1].ingredients == ["pinch of salt"]
    assert component.steps[2].ingredients is None


def test_form1_with_metadata():
    recipe_text = """---
Prep Time: 2 minutes
Cook Time: 3 minutes
Servings: 1
---
= Quick Omelette

- 2 eggs
- 1 tbsp milk
- salt and pepper

# Beat eggs with milk
# Pour into hot pan
# Fold and serve
"""
    result = parse_recipe(recipe_text)

    assert result.title == "Quick Omelette"
    assert hasattr(result, 'metadata')
    assert result.metadata["Prep Time"] == "2 minutes"
    assert result.metadata["Cook Time"] == "3 minutes"
    assert result.metadata["Servings"] == 1
    assert len(result.components) == 1

    component = result.components[0]
    assert component.name is None
    assert component.ingredients == ["2 eggs", "1 tbsp milk", "salt and pepper"]
    assert len(component.steps) == 3
    assert component.steps[0].text == "Beat eggs with milk"
    assert component.steps[1].text == "Pour into hot pan"
    assert component.steps[2].text == "Fold and serve"

    for step in component.steps:
        assert step.ingredients is None


def test_form2_with_metadata():
    recipe_text = """---
Prep Time: 1 minute
Cook Time: 4 minutes
Caffeine: 40mg
---
= Tea

# Heat water
  - 1 cup water

# Steep tea
  - 1 tea bag

# Add honey if desired
  - 1 tsp honey
"""
    result = parse_recipe(recipe_text)

    assert result.title == "Tea"
    assert hasattr(result, 'metadata')
    assert result.metadata["Prep Time"] == "1 minute"
    assert result.metadata["Cook Time"] == "4 minutes"
    assert result.metadata["Caffeine"] == "40mg"
    assert len(result.components) == 1

    component = result.components[0]
    assert component.name is None
    assert component.ingredients is None
    assert len(component.steps) == 3

    assert component.steps[0].text == "Heat water"
    assert component.steps[0].ingredients == ["1 cup water"]

    assert component.steps[1].text == "Steep tea"
    assert component.steps[1].ingredients == ["1 tea bag"]

    assert component.steps[2].text == "Add honey if desired"
    assert component.steps[2].ingredients == ["1 tsp honey"]


def test_form3_with_metadata():
    recipe_text = """---
Prep Time: 5 minutes
Servings: 2
Dietary: Vegan
---
= Snack Plate

+ Hummus

- 1 can chickpeas
- 2 tbsp tahini

# Blend ingredients

+ Veggies

- 1 carrot
- 1 celery stalk

# Cut into sticks
"""
    result = parse_recipe(recipe_text)

    assert result.title == "Snack Plate"
    assert hasattr(result, 'metadata')
    assert result.metadata["Prep Time"] == "5 minutes"
    assert result.metadata["Servings"] == 2
    assert result.metadata["Dietary"] == "Vegan"
    assert len(result.components) == 2

    hummus = result.components[0]
    assert hummus.name == "Hummus"
    assert hummus.ingredients == ["1 can chickpeas", "2 tbsp tahini"]
    assert len(hummus.steps) == 1
    assert hummus.steps[0].text == "Blend ingredients"

    veggies = result.components[1]
    assert veggies.name == "Veggies"
    assert veggies.ingredients == ["1 carrot", "1 celery stalk"]
    assert len(veggies.steps) == 1
    assert veggies.steps[0].text == "Cut into sticks"


def test_form4_with_metadata():
    recipe_text = """---
Cook Time: 15 minutes
Servings: 4
Difficulty: Easy
---
= Simple Tacos

+ Meat

# Cook ground beef
  - 1 lb ground beef
  - 1 tsp cumin

# Season
  - salt to taste

+ Assembly

# Warm tortillas
  - 4 tortillas

# Fill tacos
"""
    result = parse_recipe(recipe_text)

    assert result.title == "Simple Tacos"
    assert hasattr(result, 'metadata')
    assert result.metadata["Cook Time"] == "15 minutes"
    assert result.metadata["Servings"] == 4
    assert result.metadata["Difficulty"] == "Easy"
    assert len(result.components) == 2

    meat = result.components[0]
    assert meat.name == "Meat"
    assert meat.ingredients is None
    assert len(meat.steps) == 2

    assert meat.steps[0].text == "Cook ground beef"
    assert meat.steps[0].ingredients == ["1 lb ground beef", "1 tsp cumin"]

    assert meat.steps[1].text == "Season"
    assert meat.steps[1].ingredients == ["salt to taste"]

    assembly = result.components[1]
    assert assembly.name == "Assembly"
    assert assembly.ingredients is None
    assert len(assembly.steps) == 2

    assert assembly.steps[0].text == "Warm tortillas"
    assert assembly.steps[0].ingredients == ["4 tortillas"]

    assert assembly.steps[1].text == "Fill tacos"
    assert assembly.steps[1].ingredients is None


def test_multiple_components_mixed_forms():
    recipe_text = """= Chicken Parmesan

+ Chicken

- 4 chicken breasts
- 1 cup breadcrumbs
- 2 eggs

# Pound chicken thin
# Dip in eggs, then breadcrumbs
# Pan fry until golden

+ Sauce

# Sauté until fragrant
  - 3 cloves garlic
  - 1 tbsp olive oil
# Add and simmer
  - 1 can crushed tomatoes
  - 1 tsp oregano
"""
    result = parse_recipe(recipe_text)

    assert result.title == "Chicken Parmesan"
    assert len(result.components) == 2

    chicken = result.components[0]
    assert chicken.name == "Chicken"
    assert chicken.ingredients == ["4 chicken breasts", "1 cup breadcrumbs", "2 eggs"]
    assert len(chicken.steps) == 3
    assert chicken.steps[0].text == "Pound chicken thin"
    assert chicken.steps[0].ingredients is None
    assert chicken.steps[1].text == "Dip in eggs, then breadcrumbs"
    assert chicken.steps[1].ingredients is None
    assert chicken.steps[2].text == "Pan fry until golden"
    assert chicken.steps[2].ingredients is None

    sauce = result.components[1]
    assert sauce.name == "Sauce"
    assert sauce.ingredients is None
    assert len(sauce.steps) == 2

    assert sauce.steps[0].text == "Sauté until fragrant"
    assert sauce.steps[0].ingredients == ["3 cloves garlic", "1 tbsp olive oil"]

    assert sauce.steps[1].text == "Add and simmer"
    assert sauce.steps[1].ingredients == ["1 can crushed tomatoes", "1 tsp oregano"]


def test_asterisk_ingredients():
    recipe_text = """= Quick Salad

* 2 cups mixed greens
* 1 tomato
* 1/2 cucumber

# Chop vegetables
# Mix with greens
# Add dressing
"""
    result = parse_recipe(recipe_text)

    assert result.title == "Quick Salad"
    assert len(result.components) == 1

    component = result.components[0]
    assert component.name is None
    assert component.ingredients == ["2 cups mixed greens", "1 tomato", "1/2 cucumber"]
    assert len(component.steps) == 3
    assert component.steps[0].text == "Chop vegetables"
    assert component.steps[1].text == "Mix with greens"
    assert component.steps[2].text == "Add dressing"


def test_simple_steps():
    recipe_text = """= Simple Soup

- 2 cups broth
- 1 onion
- 2 carrots

# Dice vegetables
# Sauté in pot
# Add broth
# Simmer 20 minutes
"""
    result = parse_recipe(recipe_text)

    assert result.title == "Simple Soup"
    assert len(result.components) == 1

    component = result.components[0]
    assert component.name is None
    assert component.ingredients == ["2 cups broth", "1 onion", "2 carrots"]
    assert len(component.steps) == 4
    assert component.steps[0].text == "Dice vegetables"
    assert component.steps[1].text == "Sauté in pot"
    assert component.steps[2].text == "Add broth"
    assert component.steps[3].text == "Simmer 20 minutes"


def test_mixed_ingredient_formats():
    recipe_text = """= Mixed Format Recipe

- 1 egg
* 2 cups flour
- 1/2 cup milk
* 1 tsp salt

# Mix dry ingredients
# Add wet ingredients
# Combine thoroughly
"""
    result = parse_recipe(recipe_text)

    assert result.title == "Mixed Format Recipe"
    assert len(result.components) == 1

    component = result.components[0]
    assert component.name is None
    assert component.ingredients == ["1 egg", "2 cups flour", "1/2 cup milk", "1 tsp salt"]
    assert len(component.steps) == 3
    assert component.steps[0].text == "Mix dry ingredients"
    assert component.steps[1].text == "Add wet ingredients"
    assert component.steps[2].text == "Combine thoroughly"


def test_asterisk_ingredients_with_step_ingredients():
    recipe_text = """= Complex Recipe

+ Batter

* 2 cups flour
* 1 tsp baking powder

# Mix dry ingredients
# Add wet ingredients
  * 1 cup milk
  * 2 eggs

+ Topping

- 1/2 cup sugar
* 1 tsp cinnamon

# Combine sugar and cinnamon
"""
    result = parse_recipe(recipe_text)

    assert result.title == "Complex Recipe"
    assert len(result.components) == 2

    batter = result.components[0]
    assert batter.name == "Batter"
    assert batter.ingredients == ["2 cups flour", "1 tsp baking powder"]
    assert len(batter.steps) == 2
    assert batter.steps[0].text == "Mix dry ingredients"
    assert batter.steps[0].ingredients is None
    assert batter.steps[1].text == "Add wet ingredients"
    assert batter.steps[1].ingredients == ["1 cup milk", "2 eggs"]

    topping = result.components[1]
    assert topping.name == "Topping"
    assert topping.ingredients == ["1/2 cup sugar", "1 tsp cinnamon"]
    assert len(topping.steps) == 1
    assert topping.steps[0].text == "Combine sugar and cinnamon"
    assert topping.steps[0].ingredients is None


def test_yaml_frontmatter_with_new_formats():
    recipe_text = """---
prep_time: 10 mins
cook_time: 30 mins
servings: 4
cuisine: Italian
---
= Pasta Primavera

* 1 lb pasta
* 2 cups mixed vegetables
- 2 tbsp olive oil
* 1/4 cup parmesan

# Cook pasta according to package
# Sauté vegetables in oil
# Combine pasta and vegetables
# Top with cheese
"""
    result = parse_recipe(recipe_text)

    assert result.title == "Pasta Primavera"
    assert result.metadata["prep_time"] == "10 mins"
    assert result.metadata["cook_time"] == "30 mins"
    assert result.metadata["servings"] == 4
    assert result.metadata["cuisine"] == "Italian"

    assert len(result.components) == 1
    component = result.components[0]
    assert component.ingredients == ["1 lb pasta", "2 cups mixed vegetables", "2 tbsp olive oil", "1/4 cup parmesan"]
    assert len(component.steps) == 4
    assert component.steps[0].text == "Cook pasta according to package"
    assert component.steps[1].text == "Sauté vegetables in oil"
    assert component.steps[2].text == "Combine pasta and vegetables"
    assert component.steps[3].text == "Top with cheese"