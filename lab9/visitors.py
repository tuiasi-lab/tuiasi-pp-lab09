"""
Vizitatori pentru parcurgerea și evaluarea AST-ului.

Design Pattern: Visitor
Separă algoritmii (parcurgere, evaluare) de structura datelor (AST).
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from lab9.ast_tree import AST


class PrintVisitor(ABC):
    """Vizitator de bază care colectează token-urile vizitate."""

    def __init__(self) -> None:
        """Inițializează lista de token-uri colectate."""
        self.rezultat: list[str | int] = []

    @abstractmethod
    def viziteaza(self, nod: AST) -> None:
        """Vizitează un nod AST (implementat în subclase).

        Args:
            nod: Nodul de vizitat.
        """
        

    def get_rezultat(self) -> list[str | int]:
        """Returnează lista token-urilor colectate.

        Returns:
            Lista de token-uri în ordinea parcurgerii.
        """
        return list(self.rezultat)

    def _valoare_nod(self, nod: AST) -> str | int:
        """Returnează valoarea unui nod: număr întreg sau operator string.

        Args:
            nod: Nodul din care se extrage valoarea.

        Returns:
            Int dacă nod este operand, str dacă este operator.
        """
        if nod.token.este_operand():
            return int(nod.token.valoare)
        return nod.token.valoare


class VisitPreOrdine(PrintVisitor):
    """Parcurgere pre-ordine: Rădăcină → Stânga → Dreapta."""

    def viziteaza(self, nod: AST) -> None:
        """Parcurge AST-ul în pre-ordine și colectează token-urile.

        Args:
            nod: Rădăcina sub-arborelui de vizitat.
        """
        # Dat ca exemplu — nu modifica
        self.rezultat.append(self._valoare_nod(nod))
        if nod.stanga:
            self.viziteaza(nod.stanga)
        if nod.dreapta:
            self.viziteaza(nod.dreapta)


class VisitInOrdine(PrintVisitor):
    """Parcurgere in-ordine: Stânga → Rădăcină → Dreapta."""

    # TODO: Implementează metoda viziteaza
    def viziteaza(self, nod: AST) -> None:
        """Parcurge AST-ul în in-ordine și colectează token-urile.

        Ordinea: vizitează stânga, apoi rădăcina, apoi dreapta.

        Args:
            nod: Rădăcina sub-arborelui de vizitat.

        Exemplu pentru "3+5":
            rezultat = [3, '+', 5]
        """
        if nod.stanga:
            self.viziteaza(nod.stanga)
            
        self.rezultat.append(self._valoare_nod(nod))
        
        if nod.dreapta:
            self.viziteaza(nod.dreapta)


class VisitPostOrdine(PrintVisitor):
    """Parcurgere post-ordine: Stânga → Dreapta → Rădăcină."""

    # TODO: Implementează metoda viziteaza
    def viziteaza(self, nod: AST) -> None:
        """Parcurge AST-ul în post-ordine și colectează token-urile.

        Ordinea: vizitează stânga, apoi dreapta, apoi rădăcina.

        Args:
            nod: Rădăcina sub-arborelui de vizitat.

        Exemplu pentru "3+5":
            rezultat = [3, 5, '+']
        """
        if nod.stanga:
            self.viziteaza(nod.stanga)
            
        if nod.dreapta:
            self.viziteaza(nod.dreapta)
            
        self.rezultat.append(self._valoare_nod(nod))


class EvaluatorVisitor:
    """Vizitator care evaluează numeric expresia din AST."""

    # TODO: Implementează metoda evalueaza
    def evalueaza(self, nod: AST) -> int | float:
        """Evaluează recursiv expresia reprezentată de AST.

        Args:
            nod: Rădăcina sub-arborelui de evaluat.

        Returns:
            Valoarea numerică a expresiei.

        Raises:
            ValueError: La împărțire prin zero.
            ZeroDivisionError: La împărțire prin zero.

        Exemplu:
            ast = ASTBuilder().Parse("3+5")
            evaluator = EvaluatorVisitor()
            assert evaluator.evalueaza(ast) == 8
        """
        if nod.este_frunza():
            return int(nod.token.valoare)

        stanga = self.evalueaza(nod.stanga)
        dreapta = self.evalueaza(nod.dreapta)
        operator = nod.token.valoare

        if operator == "+":
            return stanga + dreapta
        elif operator == "-":
            return stanga - dreapta
        elif operator == "*":
            return stanga * dreapta
        elif operator == "/":
            if dreapta == 0:
                raise ZeroDivisionError("Impartire prin zero")
            return stanga / dreapta
            
        raise ValueError(f"Operator necunoscut: {operator}")
