# Smidge

A plain-text file format for structured recipes, a Python library for parsing, and a command-line application for converting them to PDFs.

## Recipe Format

The Smidge format is a simple, structured way to write recipes in plain text files that's easy to read and write.

### Two Forms

Recipes can be written in two fundamental forms, depending on how you organize ingredients and instructions.

In the first form, you list all ingredients up front, then provide the instructions:

```recipe
= Classic Brownies

- 1 cup butter
- 2 cups sugar
- 4 eggs
- 3/4 cup cocoa powder
- 1 cup flour

# Melt butter and mix with sugar
# Beat in eggs one at a time
# Fold in cocoa and flour
# Bake 25 minutes at 350 °F
```

In the second form, you include ingredients within the instructions as they're needed:

```recipe
= Classic Brownies

# Melt and mix
  - 1 cup butter
  - 2 cups sugar
# Beat in one at a time
  - 4 eggs
# Fold in dry ingredients
  - 3/4 cup cocoa powder
  - 1 cup flour
# Bake 25 minutes at 350 °F
```

The parser recognizes ingredients nested under steps when they're indented exactly 2 spaces.

### Ingredients

Ingredients are prefixed with a dash (`-`).

```recipe
= Recipe

- 2 cups flour
- 1 cup sugar
- 1/2 tsp salt
- 2 eggs
```

### Steps

Steps are marked with a hash symbol (`#`):

```recipe
= Recipe

# Mix dry ingredients
# Add wet ingredients
# Combine thoroughly
```

### Multiple Components

Both forms support multiple components. A plus (`+`) prefix creates named components:

```recipe
= Chicken Parmesan

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
```

Each component can use either form independently.

### Metadata

Recipe metadata uses YAML frontmatter format:

```text
---
Prep Time: 20 minutes
Cook Time: 45 minutes
Servings: 6
---
```

Metadata must appear at the very beginning of your recipe file, before the title. The YAML frontmatter is delimited by three dashes (`---`) at the start and end of the metadata section.

## Python Library

The `smidge` library provides classes and functions for parsing recipe files into structured Python objects.

### parse_recipe()

Parses a recipe from text and returns a `Recipe` object.

```python
from smidge import parse_recipe

recipe_text = """
---
Prep Time: 10 minutes
---
= Simple Salad

- Mixed greens
- Cherry tomatoes
- Olive oil

# Wash greens
# Add tomatoes
# Drizzle with oil
"""

recipe = parse_recipe(recipe_text)
print(recipe.title)  # "Simple Salad"
```

Returns `None` if the recipe cannot be parsed (e.g., missing title).

### Models

```python
@dataclass
class Step:
    text: str
    ingredients: list[str] | None


@dataclass
class Component:
    name: str | None
    ingredients: list[str] | None
    steps: list[Step]


@dataclass
class Recipe:
    title: str
    components: list[Component]
    metadata: dict[str, str]
```

### Example Usage

```python
from smidge import parse_recipe

with open('my_recipe.recipe', 'r') as f:
    recipe_text = f.read()

recipe = parse_recipe(recipe_text)

print(f"Recipe: {recipe.title}")

for key, value in recipe.metadata.items():
    print(f"{key}: {value}")

for component in recipe.components:
    if component.name:
        print(f"\n{component.name}:")
    
    if component.ingredients:
        print("Ingredients:")
        for ingredient in component.ingredients:
            print(f"  - {ingredient}")
    
    print("Steps:")
    for i, step in enumerate(component.steps, 1):
        print(f"  {i}. {step.text}")
        if step.ingredients:
            for ingredient in step.ingredients:
                print(f"     - {ingredient}")
```

## Command-Line Application

The `smidge` command-line tool provides utilities for working with recipe files.

### Installation

Install the smidge package, then use the `smidge` command:

```bash
smidge --help
```

### Converting to PDF

Convert a recipe file to a PDF:

```bash
smidge pdf banana-bread.md
```

Specify a custom output path:

```bash
smidge pdf banana-bread.md -o cookbook/banana-bread.pdf
```

Convert multiple recipes into a cookbook with a custom title:

```bash
smidge pdf *.recipe -t "Family Recipes"
```

Add a subtitle and cover image:

```bash
smidge pdf *.recipe -t "Holiday Cookbook" -s "December 2024" -i cover.jpg
```

### Printing Recipes

Send a recipe directly to the printer:

```bash
smidge print banana-bread.md
```

Print a cookbook with custom formatting:

```bash
smidge print *.recipe -t "Weekend Meals" -s "Quick and Easy" -i food.jpg
```

### Command Options

Both `pdf` and `print` commands support:

- `-t, --title`: Set the cookbook title (default: "Cookbook")
- `-s, --subtitle`: Add a subtitle to the cover page
- `-i, --image`: Add a cover image
