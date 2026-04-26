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

    def Parse(self, expresie: str) -> AST:
        """Parsează o expresie aritmetică și returnează AST-ul corespunzător.

        Folosește o abordare iterativă în două treceri:
        1. Tokenizare
        2. Construire AST respectând prioritatea operatorilor

        Args:
            expresie: Expresia de parsare (ex: "3+5*2", "10-3+1").

        Returns:
            Rădăcina arborelui AST.
        """
        tokens = self._tokenizeaza(expresie)
        return self._parse_expresie(tokens, 0)[0]

    def _tokenizeaza(self, expresie: str) -> list[Token]:
        """Transformă expresia în listă de token-uri.

        Args:
            expresie: Expresia de tokenizat.

        Returns:
            Lista de token-uri.
        """
        tokens = []
        i = 0
        while i < len(expresie):
            if expresie[i] in {"+", "-", "*", "/"}:
                tokens.append(Token(expresie[i]))
                i += 1
            elif expresie[i].isdigit():
                j = i
                while j < len(expresie) and expresie[j].isdigit():
                    j += 1
                tokens.append(Token(expresie[i:j]))
                i = j
            else:
                i += 1
        return tokens

    def _parse_expresie(self, tokens: list[Token], pos: int) -> tuple[AST, int]:
        """Parsează o expresie (sumă/diferență de termeni).

        expresie := termen (('+' | '-') termen)*

        Args:
            tokens: Lista de token-uri.
            pos: Poziția curentă în lista de token-uri.

        Returns:
            Tuplu (nod AST, poziție după parsare).
        """
        # Parsăm primul termen
        stanga, pos = self._parse_termen(tokens, pos)

        # Continuăm cât timp urmează + sau -
        while pos < len(tokens) and tokens[pos].valoare in {"+", "-"}:
            operator = tokens[pos]
            pos += 1
            dreapta, pos = self._parse_termen(tokens, pos)
            stanga = AST(token=operator, stanga=stanga, dreapta=dreapta)

        return stanga, pos

    def _parse_termen(self, tokens: list[Token], pos: int) -> tuple[AST, int]:
        """Parsează un termen (produs/câit de factori).

        termen := factor (('*' | '/') factor)*

        Args:
            tokens: Lista de token-uri.
            pos: Poziția curentă în lista de token-uri.

        Returns:
            Tuplu (nod AST, poziție după parsare).
        """
        # Parsăm primul factor
        stanga, pos = self._parse_factor(tokens, pos)

        # Continuăm cât timp urmează * sau /
        while pos < len(tokens) and tokens[pos].valoare in {"*", "/"}:
            operator = tokens[pos]
            pos += 1
            dreapta, pos = self._parse_factor(tokens, pos)
            stanga = AST(token=operator, stanga=stanga, dreapta=dreapta)

        return stanga, pos

    def _parse_factor(self, tokens: list[Token], pos: int) -> tuple[AST, int]:
        """Parsează un factor (număr întreg).

        factor := NUMAR

        Args:
            tokens: Lista de token-uri.
            pos: Poziția curentă în lista de token-uri.

        Returns:
            Tuplu (nod AST frunză, poziție după parsare).
        """
        token = tokens[pos]
        return AST(token=token), pos + 1
