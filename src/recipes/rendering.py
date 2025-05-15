from collections import defaultdict


def recipe_to_typst(recipes, title: str | None = None, subtitle: str | None = None, image: str | None = None) -> str:
    if len(recipes) == 1:
        return _render_single_recipe(recipes[0])

    typst = "#set text(\n"
    typst += "  font: \"Source Serif Pro\",\n"
    typst += "  size: 12pt\n"
    typst += ")\n\n"
    typst += "#set page(\n"
    typst += "  margin: 2cm\n"
    typst += ")\n\n"

    if title or subtitle or image:
        typst += "#v(2em)"

        if title:
            typst += "#align(center)[\n"
            typst += "  #text(size: 22pt)[\n"
            typst += f"    #heading(level: 2, outlined: false)[{title}]\n"
            typst += "  ]\n"
            typst += "]\n"
            typst += "#v(1cm)\n\n"

        if subtitle:
            typst += "#align(center)[\n"
            typst += f"  #heading(level: 3, outlined: false)[{subtitle}]\n"
            typst += "]\n"
            typst += "#v(1cm)\n\n"

        if image:
            typst += "#v(1em)\n"
            typst += "#figure(\n"
            typst += f"  image(\"{image}\", width: 80%),\n"
            typst += ")\n"

        typst += "#pagebreak()"

    typst += "#align(center)[\n"
    typst += "  #heading(level: 2, outlined: false)[Contents]\n"
    typst += "]\n"
    typst += "#v(1cm)\n\n"
    typst += "#outline(\n"
    typst += "  title: none,\n"
    typst += "  depth: 2\n"
    typst += ")\n#pagebreak()\n\n"
    typst += "#counter(page).update(1)\n\n"

    recipes_by_category = defaultdict(list)
    for recipe in recipes:
        category = recipe.metadata.get('Category', 'Uncategorized') if hasattr(recipe, 'metadata') and recipe.metadata else 'Uncategorized'
        recipes_by_category[category].append(recipe)

    for category_index, (category, category_recipes) in enumerate(sorted(recipes_by_category.items())):
        typst += "#set page(\n"
        typst += "  footer: context [\n"
        typst += "    #h(1fr)\n"
        typst += "    #counter(page).display() / #counter(page).final().at(0)\n"
        typst += "    #h(1fr)\n"
        typst += "  ]\n"
        typst += ")\n"
        typst += "#v(2cm)\n"
        typst += "#align(center)[\n"
        typst += f"  #heading(level: 1)[{category}]\n"
        typst += "]\n"
        typst += "#pagebreak()\n\n"

        for i, recipe in enumerate(category_recipes):
            typst += _render_single_recipe(recipe)
            if i < len(category_recipes) - 1:
                typst += "\n#pagebreak()\n\n"

        if category_index < len(recipes_by_category) - 1:
            typst += "\n#pagebreak()\n\n"

    return typst


def _render_single_recipe(recipe):
    source_value = recipe.metadata.get('Source') if hasattr(recipe, 'metadata') and recipe.metadata else None

    typst = "#set list(\n spacing: 0.65em,\n)\n\n"

    typst += "#set page(\n"
    typst += "  footer: context [\n"
    if source_value:
        typst += f"    {source_value}\n"
        typst += "    #h(1fr)\n"
        typst += "    #counter(page).display() / #counter(page).final().at(0)\n"
    else:
        typst += "    #h(1fr)\n"
        typst += "    #counter(page).display() / #counter(page).final().at(0)\n"
        typst += "    #h(1fr)\n"
    typst += "  ]\n"
    typst += ")\n\n"

    typst += f"#align(center)[== {recipe.title}]\n"
    typst += "#v(2em)\n\n"

    if hasattr(recipe, 'metadata') and recipe.metadata:
        regular_metadata = {k: v for k, v in recipe.metadata.items() if k != 'Source'}

        if regular_metadata:
            metadata_items = list(regular_metadata.items())

            typst += "#align(center)[\n"
            typst += "#text(size: 0.80em, fill: rgb(\"#222222\"))[\n"

            for chunk_start in range(0, len(metadata_items), 5):
                chunk_end = min(chunk_start + 5, len(metadata_items))
                chunk = metadata_items[chunk_start:chunk_end]

                typst += "#grid(\n"
                typst += " columns: (auto, auto, auto, auto, auto),\n"
                typst += " column-gutter: 3em,\n"
                typst += " row-gutter: 1em,\n"

                typst += " "
                for key, _ in chunk:
                    typst += f"[*{key}*],\n "
                for _ in range(5 - len(chunk)):
                    typst += "[],\n "

                for _, value in chunk:
                    typst += f"[{value}],\n "
                for _ in range(5 - len(chunk)):
                    typst += "[],\n "

                typst = typst[:-2] + "\n"
                typst += ")\n"

                if chunk_end < len(metadata_items):
                    typst += "#v(1em)\n\n"

            typst += "]\n"
            typst += "]\n"

        typst += "#v(2em)\n\n"

    for component_index, component in enumerate(recipe.components):
        if component.name:
            typst += f"=== {component.name}\n"
            typst += "#v(1em)\n\n"

        has_step_ingredients = any(step.ingredients for step in component.steps)

        if not has_step_ingredients:
            typst += "#grid(\n"
            typst += " columns: (1.3fr, 1fr),\n"
            typst += " gutter: 3em,\n"
            typst += " \n"
            typst += " [   \n"
            typst += "   #enum(\n"
            typst += "     spacing: 1.5em,\n"
            typst += "     \n"
            for step in component.steps:
                typst += f"     [{step.text}],\n"
            typst += "   )\n"
            typst += " ],\n"
            typst += " \n"
            typst += " [  \n"
            if component.ingredients:
                typst += "   #list(\n"
                typst += "     spacing: 1em,\n"
                for ingredient in component.ingredients:
                    typst += f"     [{ingredient}],\n"
                typst += "   )\n"
            typst += " ]\n"
            typst += ")\n"

        else:
            for step_index, step in enumerate(component.steps):
                typst += "#grid(\n"
                typst += " columns: (1.3fr, 1fr),\n"
                typst += " gutter: 3em, \n"
                typst += " \n"
                typst += " [  \n"
                typst += "   #enum(\n"
                typst += "     spacing: 1.5em,\n"
                typst += "     \n"
                typst += f"     enum.item({step_index + 1})[{step.text}],\n"
                typst += "   )\n"
                typst += " ], \n"
                typst += " \n"
                typst += " [\n"
                if step.ingredients:
                    typst += "  \n"
                    typst += "   #list(\n"
                    typst += "     spacing: 1em,\n"
                    for ingredient in step.ingredients:
                        typst += f"     [{ingredient}],\n"
                    typst += "   )\n"
                typst += " ]\n"
                typst += ")\n"

                if step_index < len(component.steps) - 1:
                    typst += "#v(1em)\n"

        if component_index < len(recipe.components) - 1:
            typst += "\n#v(3em)\n\n"

    return typst