from dataclasses import dataclass, field
import yaml


@dataclass
class Step:
    text: str
    ingredients: list[str] | None = None


@dataclass
class Component:
    name: str | None = None
    ingredients: list[str] | None = None
    steps: list[Step] = field(default_factory=list)


@dataclass
class Recipe:
    title: str
    components: list[Component]
    metadata: dict[str, str] = field(default_factory=dict)


def parse_recipe(recipe_text):
    lines = recipe_text.strip().split('\n')

    metadata = {}
    content_start = 0

    if lines and lines[0].strip() == '---':
        for i, line in enumerate(lines[1:], 1):
            if line.strip() == '---':
                frontmatter = '\n'.join(lines[1:i])
                metadata = yaml.safe_load(frontmatter) or {}
                content_start = i + 1
                break

    lines = lines[content_start:]

    recipe_title = None
    components = []
    current_component = None
    current_step = None
    has_subtitles = False

    for line in lines:
        if line.strip() and line.lstrip().startswith('+ '):
            has_subtitles = True
            break

    for line in lines:
        stripped = line.strip()

        if not stripped:
            continue

        stripped_left = line.lstrip()

        if stripped_left.startswith('= '):
            recipe_title = stripped_left[2:].strip()

            if not has_subtitles:
                current_component = Component(name=None)
                components.append(current_component)

        elif stripped_left.startswith('+ '):
            component_name = stripped_left[2:].strip()
            current_component = Component(name=component_name)
            components.append(current_component)

        elif stripped_left.startswith('- ') or stripped_left.startswith('* '):
            ingredient = stripped_left[2:].strip()

            indent = len(line) - len(stripped_left)

            if indent == 2 and current_step is not None:
                if current_step.ingredients is None:
                    current_step.ingredients = []
                current_step.ingredients.append(ingredient)
            else:
                if current_component is not None:
                    if current_component.ingredients is None:
                        current_component.ingredients = []
                    current_component.ingredients.append(ingredient)

        elif stripped_left.startswith('# '):
            step_text = stripped_left[2:].strip()
            step = Step(text=step_text)
            if current_component is not None:
                current_component.steps.append(step)
                current_step = step

    if recipe_title is None:
        return None

    return Recipe(title=recipe_title, components=components, metadata=metadata)
