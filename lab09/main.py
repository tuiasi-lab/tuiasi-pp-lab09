"""
Entry point pentru demonstrarea AST-ului cu vizitatori.

Utilizare:
    uv run python -m lab9.main
"""

from lab9.ast_tree import ASTBuilder
from lab9.visitors import VisitPreOrdine, VisitInOrdine, VisitPostOrdine, EvaluatorVisitor
from lab9.recursive_builder import RecursiveASTBuilder
from lab9.log import Log


def main() -> None:
    """Demonstrează funcționalitatea AST-ului cu diferite vizitatori."""
    log = Log.get_instance()

    expresii = ["3+5", "10-3", "3+5*2", "10-3+1"]

    for expresie in expresii:
        log.log(f"Parsez expresia: {expresie}")
        print(f"\nExpresie: {expresie}")

        builder = ASTBuilder()
        ast = builder.Parse(expresie)

        # Pre-ordine
        pre = VisitPreOrdine()
        pre.viziteaza(ast)
        print(f"  Pre-ordine:  {pre.get_rezultat()}")

        # In-ordine
        ino = VisitInOrdine()
        ino.viziteaza(ast)
        print(f"  In-ordine:   {ino.get_rezultat()}")

        # Post-ordine
        post = VisitPostOrdine()
        post.viziteaza(ast)
        print(f"  Post-ordine: {post.get_rezultat()}")

        # Evaluare
        evaluator = EvaluatorVisitor()
        valoare = evaluator.evalueaza(ast)
        print(f"  Valoare:     {valoare}")

    print("\n--- Versiunea recursivă ---")
    recursive = RecursiveASTBuilder()
    ast2 = recursive.Parse("3+5-2")
    ino2 = VisitInOrdine()
    ino2.viziteaza(ast2)
    print(f"  3+5-2 in-ordine: {ino2.get_rezultat()}")

    print("\n--- Log Singleton ---")
    print(f"  Total mesaje înregistrate: {len(Log.get_instance().get_mesaje())}")


if __name__ == "__main__":
    main()
