"""
AST (Abstract Syntax Tree) pentru expresii aritmetice.

Suportă operatori: +, -, *, /
Respectă prioritățile operatorilor (* și / au prioritate față de + și -).

Design Pattern: Composite (nodul AST)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Token:
    """Token dintr-o expresie aritmetică."""

    valoare: str  # Ex: "+", "-", "*", "/", "3", "15"

    def este_operator(self) -> bool:
        """Returnează True dacă token-ul este un operator."""
        return self.valoare in {"+", "-", "*", "/"}

    def este_operand(self) -> bool:
        """Returnează True dacă token-ul este un număr."""
        return not self.este_operator()


@dataclass
class AST:
    """Nod din arborele sintactic abstract.

    Un nod poate fi:
    - Operator (nod intern cu copii stânga și dreapta)
    - Operand / Frunză (nod terminal cu valoare numerică)
    """

    token: Token
    stanga: Optional["AST"] = field(default=None)
    dreapta: Optional["AST"] = field(default=None)

    def este_frunza(self) -> bool:
        """Returnează True dacă nodul este o frunză (operand)."""
        return self.stanga is None and self.dreapta is None


# Alias pentru compatibilitate
Operator = AST
Operand = AST


class ASTBuilder:
    """Construiește un AST dintr-o expresie aritmetică.

    Respectă prioritatea operatorilor:
    - * și / au prioritate față de + și -
    - Evaluare de la stânga la dreapta pentru operatori de aceeași prioritate

    Presupuneri:
    - Expresia nu conține spații
    - Operanzii sunt numere întregi non-negative
    - Expresia este validă sintactic
    """

    # TODO: Implementează metoda Parse
    def Parse(self, expresie: str) -> AST:
        """Parsează o expresie aritmetică și returnează AST-ul corespunzător.

        Exemplu:
            builder = ASTBuilder()
            ast = builder.Parse("3+5")
            # Returnează un nod AST cu token '+', stânga=3, dreapta=5

        Args:
            expresie: Expresia de parsare (ex: "3+5*2", "10-3+1").

        Returns:
            Rădăcina arborelui AST.

        Hint:
            Parsează mai întâi + și -, apoi * și /.
            Folosește o abordare iterativă cu stivă sau recursivă.
        """
        raise NotImplementedError("De implementat")
