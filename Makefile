SUBDIR := github_stars

.PHONY: format format-check ruff mypy pyrefly test lint lint-check run

format format-check ruff mypy pyrefly test lint lint-check run:
	$(MAKE) -C $(SUBDIR) $@