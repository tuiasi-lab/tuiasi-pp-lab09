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
        """Vizitează un nod AST (implementat în subclase)."""
        ...

    def get_rezultat(self) -> list[str | int]:
        """Returnează lista token-urilor colectate."""
        return list(self.rezultat)

    def _valoare_nod(self, nod: AST) -> str | int:
        """Returnează valoarea unui nod: număr întreg sau operator string."""
        if nod.token.este_operand():
            return int(nod.token.valoare)
        return nod.token.valoare


class VisitPreOrdine(PrintVisitor):
    """Parcurgere pre-ordine: Rădăcină → Stânga → Dreapta."""

    def viziteaza(self, nod: AST) -> None:
        # Dat ca exemplu — nu modifica
        self.rezultat.append(self._valoare_nod(nod))
        if nod.stanga:
            self.viziteaza(nod.stanga)
        if nod.dreapta:
            self.viziteaza(nod.dreapta)


class VisitInOrdine(PrintVisitor):
    """Parcurgere in-ordine: Stânga → Rădăcină → Dreapta."""

    def viziteaza(self, nod: AST) -> None:
        """Parcurge AST-ul în in-ordine și colectează token-urile.

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

    def viziteaza(self, nod: AST) -> None:
        """Parcurge AST-ul în post-ordine și colectează token-urile.

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

    def evalueaza(self, nod: AST) -> int | float:
        """Evaluează recursiv expresia reprezentată de AST.

        Args:
            nod: Rădăcina sub-arborelui de evaluat.

        Returns:
            Valoarea numerică a expresiei.

        Raises:
            ZeroDivisionError: La împărțire prin zero.
        """
        # Frunză → returnează valoarea numerică
        if nod.este_frunza():
            return int(nod.token.valoare)

        # Nod intern → evaluează recursiv copiii
        val_stanga = self.evalueaza(nod.stanga)
        val_dreapta = self.evalueaza(nod.dreapta)

        op = nod.token.valoare
        if op == "+":
            return val_stanga + val_dreapta
        elif op == "-":
            return val_stanga - val_dreapta
        elif op == "*":
            return val_stanga * val_dreapta
        elif op == "/":
            if val_dreapta == 0:
                raise ZeroDivisionError("Împărțire prin zero")
            return val_stanga / val_dreapta
        else:
            raise ValueError(f"Operator necunoscut: {op}")
