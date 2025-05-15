.PHONY: build install clean

build: bin/recipes

bin/recipes: src/recipes/*.py
	mkdir -p bin
	uv run nuitka \
		--onefile \
		--output-dir=bin \
		--output-filename=recipes \
		--include-package=src.recipes \
		src/recipes/main.py

install: build
	mkdir -p ~/.local/bin
	cp bin/recipes ~/.local/bin/

clean:
	rm -rf bin
