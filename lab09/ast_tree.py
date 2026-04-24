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
    """Nod din arborele sintactic abstract."""

    token: Token
    stanga: Optional["AST"] = field(default=None)
    dreapta: Optional["AST"] = field(default=None)

    def este_frunza(self) -> bool:
        return self.stanga is None and self.dreapta is None


# Alias pentru compatibilitate
Operator = AST
Operand = AST


class ASTBuilder:
    """Construiește un AST dintr-o expresie aritmetică."""

    def Parse(self, expresie: str) -> AST:
        # 1. Căutăm operatori de prioritate mică (+ și -)
        for i in range(len(expresie) - 1, -1, -1):
            if expresie[i] in "+-":
                stanga = expresie[:i]
                dreapta = expresie[i + 1:]

                return AST(
                    Token(expresie[i]),
                    self.Parse(stanga),
                    self.Parse(dreapta)
                )

        # 2. Dacă nu găsim, căutăm operatori de prioritate mare (* și /)
        for i in range(len(expresie) - 1, -1, -1):
            if expresie[i] in "*/":
                stanga = expresie[:i]
                dreapta = expresie[i + 1:]

                return AST(
                    Token(expresie[i]),
                    self.Parse(stanga),
                    self.Parse(dreapta)
                )

        # 3. Caz de bază: este un număr (frunză)
        return AST(Token(expresie))
