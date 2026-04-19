# Lab 9 — Python Design Patterns (Singleton, Visitor, AST)

## Descriere

Implementează un **arbore sintactic abstract (AST)** pentru expresii aritmetice, împreună cu vizitatori pentru parcurgerea și evaluarea sa. Aplică pattern-ul **Singleton** pentru un sistem de jurnalizare.

## Structura proiectului

```
lab09/
  lab9/
    __init__.py
    log.py               ← Singleton Log (stub)
    ast_tree.py          ← Token, AST, ASTBuilder (stub)
    visitors.py          ← vizitatori (pre/in/post/evaluator) (stub)
    recursive_builder.py ← RecursiveASTBuilder (stub)
    main.py              ← entry point
  tests/
    __init__.py
    test_lab9.py         ← teste complete
  .github/workflows/classroom.yml
  pyproject.toml
  ASSIGNMENT.md
  README.md
```

## Cerințe

### Tema 1 — AST cu vizitatori + priorități operatori

#### 1.1 `log.py` — Singleton `Log`

Implementează pattern-ul Singleton:

```python
log1 = Log.get_instance()
log2 = Log.get_instance()
assert log1 is log2  # Aceeași instanță!

log1.log("Mesaj")
print(log2.get_mesaje())  # ['[2026-04-19 10:00:00] Mesaj']
```

**Cerințe:**
- `get_instance()` returnează **întotdeauna** același obiect
- `log(mesaj)` adaugă mesajul cu timestamp la lista internă
- `get_mesaje()` returnează copia listei de mesaje
- `sterge_mesaje()` golește lista

#### 1.2 `ast_tree.py` — `ASTBuilder.Parse()`

Implementează parsarea cu **prioritate operatori**:

```
"3+5*2" → AST:
         +
        / \
       3   *
          / \
         5   2
```

Evaluare: `3 + (5 * 2) = 13` (NU `(3+5) * 2 = 16`)

**Hint algoritm:**
- Parsează mai întâi operatorii cu prioritate scăzută (`+`, `-`)
- Fiecare operand din suma este un "termen" (produs/câit)
- Operatorii `*` și `/` leagă mai strâns

#### 1.3 `visitors.py` — Vizitatori

| Vizitator | Ordine | Exemplu pentru "3+5" |
|-----------|--------|----------------------|
| `VisitPreOrdine` | Rădăcină → Stânga → Dreapta | `['+', 3, 5]` |
| `VisitInOrdine` | Stânga → Rădăcină → Dreapta | `[3, '+', 5]` |
| `VisitPostOrdine` | Stânga → Dreapta → Rădăcină | `[3, 5, '+']` |
| `EvaluatorVisitor` | (calcul recursiv) | `8` |

**`EvaluatorVisitor.evalueaza(nod)`:**

```python
evaluator = EvaluatorVisitor()
ast = ASTBuilder().Parse("3+5*2")
assert evaluator.evalueaza(ast) == 13
```

Algoritmul:
1. Dacă nodul este frunză → returnează `int(nod.token.valoare)`
2. Altfel → evaluează recursiv stânga și dreapta, aplică operatorul

### Tema 2 — `RecursiveASTBuilder`

Implementează aceeași funcționalitate ca `ASTBuilder` dar **recursiv**.

**Gramatică (EBNF):**
```
expresie := termen (('+' | '-') termen)*
termen   := factor (('*' | '/') factor)*
factor   := NUMAR
```

```python
ast1 = ASTBuilder().Parse("3+5-2")
ast2 = RecursiveASTBuilder().Parse("3+5-2")

# Ambele produc același AST → același rezultat la parcurgere
ino1 = VisitInOrdine(); ino1.viziteaza(ast1)
ino2 = VisitInOrdine(); ino2.viziteaza(ast2)
assert ino1.get_rezultat() == ino2.get_rezultat()
```

## Exemple de utilizare

### Rulare demonstrație:
```bash
uv run python -m lab9.main
```

**Output exemplu:**
```
Expresie: 3+5
  Pre-ordine:  ['+', 3, 5]
  In-ordine:   [3, '+', 5]
  Post-ordine: [3, 5, '+']
  Valoare:     8

Expresie: 3+5*2
  Pre-ordine:  ['+', 3, '*', 5, 2]
  In-ordine:   [3, '+', 5, '*', 2]
  Post-ordine: [3, 5, 2, '*', '+']
  Valoare:     13
```

### Rulare teste:
```bash
uv run pytest
uv run pytest -v
```

## Tabel evaluare

| Cerință | Punctaj |
|---------|---------|
| `Log` Singleton — `get_instance()` | 10p |
| `Log.log()` cu timestamp | 5p |
| `ASTBuilder.Parse()` — adunare/scădere | 15p |
| `ASTBuilder.Parse()` — prioritate `*`/`/` | 15p |
| `VisitInOrdine` corect | 10p |
| `VisitPostOrdine` corect | 10p |
| `EvaluatorVisitor` — +/- corect | 10p |
| `EvaluatorVisitor` — */÷ corect | 10p |
| `RecursiveASTBuilder` — același rezultat | 15p |
| **Total** | **100p** |

## Resurse

- [Design Pattern Visitor — Wikipedia](https://en.wikipedia.org/wiki/Visitor_pattern)
- [Design Pattern Singleton — Wikipedia](https://en.wikipedia.org/wiki/Singleton_pattern)
- [Abstract Syntax Tree — Wikipedia](https://en.wikipedia.org/wiki/Abstract_syntax_tree)
- [Recursive Descent Parsing](https://en.wikipedia.org/wiki/Recursive_descent_parser)
