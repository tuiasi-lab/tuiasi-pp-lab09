# Lab 9 — Python Design Patterns (Singleton, Visitor, AST)

Template GitHub Classroom pentru laboratorul 9 de Programare Python.

## Conținut

- **`lab9/log.py`** — Singleton Log (stub de implementat)
- **`lab9/ast_tree.py`** — Token, AST, ASTBuilder cu prioritate operatori (stub)
- **`lab9/visitors.py`** — Vizitatori pre/in/post-ordine + EvaluatorVisitor (stub)
- **`lab9/recursive_builder.py`** — Versiunea recursivă a ASTBuilder (stub)
- **`lab9/main.py`** — Entry point demonstrativ
- **`tests/test_lab9.py`** — Suite de teste (nu modifica)

## Cum se rulează

```bash
# Rulare teste
uv run pytest

# Rulare cu output detaliat
uv run pytest -v

# Demonstrație completă
uv run python -m lab9.main
```

## Cum se instalează dependențele

```bash
uv sync
```

## Cerințe

- Python >= 3.11
- uv (package manager)
