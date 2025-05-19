import argparse
import subprocess
import tempfile
from pathlib import Path

from src.smidge import parse_recipe, Recipe
from src.smidge.rendering import recipe_to_typst


def build_pdf(typst_code: str, output_path: Path, image_path=None):
    temp_typst = output_path.with_suffix('.typ')

    if image_path:
        image_path = Path(image_path)
        rel_image_path = image_path.relative_to(temp_typst.parent) if image_path.is_absolute() else image_path
        typst_code = typst_code.replace(str(image_path), str(rel_image_path))

    temp_typst.write_text(typst_code)
    subprocess.run(['typst', 'compile', '--root', '/', str(temp_typst), str(output_path)])
    temp_typst.unlink()


def load_recipes(input_files: list[str]) -> list[Recipe]:
    recipes = []
    for input_file in input_files:
        input_path = Path(input_file)
        recipe_text = input_path.read_text()
        recipe = parse_recipe(recipe_text)
        if recipe:
            recipes.append(recipe)
    return recipes


def pdf_command(args: argparse.Namespace):
    recipes = load_recipes(args.input)

    if args.output:
        output_path = Path(args.output)
    elif len(args.input) == 1:
        output_path = Path(args.input[0]).with_suffix('.pdf')
    else:
        output_path = Path('smidge.pdf')

    typst_code = recipe_to_typst(recipes, title=args.title, subtitle=args.subtitle, image=args.image)
    build_pdf(typst_code, output_path)


def print_command(args: argparse.Namespace):
    recipes = load_recipes(args.input)
    typst_code = recipe_to_typst(recipes, title=args.title, subtitle=args.subtitle, image=args.image)

    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
        tmp_path = Path(tmp.name)

    try:
        build_pdf(typst_code, tmp_path)
        subprocess.run(['lp', str(tmp_path)])
    finally:
        tmp_path.unlink()


def main():
    parser = argparse.ArgumentParser(prog='smidge')
    subparsers = parser.add_subparsers(dest='command', required=True)

    pdf_parser = subparsers.add_parser('pdf', help='Convert recipe to PDF')
    pdf_parser.add_argument('input', nargs='+', help='Input recipe file(s)')
    pdf_parser.add_argument('-o', '--output', help='Output PDF file')
    pdf_parser.add_argument('-t', '--title', default='Cookbook', help='Title for the cookbook (default: Cookbook)')
    pdf_parser.add_argument('-s', '--subtitle', help='Subtitle for the cookbook')
    pdf_parser.add_argument('-i', '--image', help='Path to cover image')
    pdf_parser.set_defaults(func=pdf_command)

    print_parser = subparsers.add_parser('print', help='Print recipe')
    print_parser.add_argument('input', nargs='+', help='Input recipe file(s)')
    print_parser.add_argument('-t', '--title', default='Cookbook', help='Title for the cookbook (default: Cookbook)')
    print_parser.add_argument('-s', '--subtitle', help='Subtitle for the cookbook')
    print_parser.add_argument('-i', '--image', help='Path to cover image')
    print_parser.set_defaults(func=print_command)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
