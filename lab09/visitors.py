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
        self.rezultat: list[str | int] = []

    @abstractmethod
    def viziteaza(self, nod: AST) -> None:
        ...

    def get_rezultat(self) -> list[str | int]:
        return list(self.rezultat)

    def _valoare_nod(self, nod: AST) -> str | int:
        if nod.token.este_operand():
            return int(nod.token.valoare)
        return nod.token.valoare


class VisitPreOrdine(PrintVisitor):
    """Rădăcină → Stânga → Dreapta"""

    def viziteaza(self, nod: AST) -> None:
        self.rezultat.append(self._valoare_nod(nod))
        if nod.stanga:
            self.viziteaza(nod.stanga)
        if nod.dreapta:
            self.viziteaza(nod.dreapta)


class VisitInOrdine(PrintVisitor):
    """Stânga → Rădăcină → Dreapta"""

    def viziteaza(self, nod: AST) -> None:
        if nod.stanga:
            self.viziteaza(nod.stanga)

        self.rezultat.append(self._valoare_nod(nod))

        if nod.dreapta:
            self.viziteaza(nod.dreapta)


class VisitPostOrdine(PrintVisitor):
    """Stânga → Dreapta → Rădăcină"""

    def viziteaza(self, nod: AST) -> None:
        if nod.stanga:
            self.viziteaza(nod.stanga)

        if nod.dreapta:
            self.viziteaza(nod.dreapta)

        self.rezultat.append(self._valoare_nod(nod))


class EvaluatorVisitor:
    """Vizitator care evaluează numeric expresia din AST."""

    def evalueaza(self, nod: AST) -> int | float:
        # dacă este frunză (număr)
        if nod.token.este_operand():
            return int(nod.token.valoare)

        # evaluăm recursiv stânga și dreapta
        st = self.evalueaza(nod.stanga)
        dr = self.evalueaza(nod.dreapta)

        op = nod.token.valoare

        if op == '+':
            return st + dr
        elif op == '-':
            return st - dr
        elif op == '*':
            return st * dr
        elif op == '/':
            if dr == 0:
                raise ZeroDivisionError("Împărțire la zero")
            return st / dr

        raise ValueError(f"Operator necunoscut: {op}")
