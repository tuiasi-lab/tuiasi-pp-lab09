"""
Versiunea recursivă a ASTBuilder.

Construiește AST-ul printr-o funcție recursivă de descent
în loc de abordarea iterativă cu stivă.
"""

from lab9.ast_tree import AST, Token


class RecursiveASTBuilder:
    """Construiește un AST printr-o funcție recursivă de descendent.

    Gramatică (EBNF):
        expresie  := termen (('+' | '-') termen)*
        termen    := factor (('*' | '/') factor)*
        factor    := NUMAR
    """

    def __init__(self) -> None:
        self._expresie: str = ""
        self._pozitie: int = 0

    def Parse(self, expresie: str) -> AST:
        self._expresie = expresie
        self._pozitie = 0
        return self._parse_expresie()

    def _parse_expresie(self) -> AST:
        nod = self._parse_termen()

        while self._caracter_curent() in ('+', '-'):
            op = self._caracter_curent()
            self._pozitie += 1  # consumam operatorul

            dreapta = self._parse_termen()
            nod = AST(Token(op), nod, dreapta)

        return nod

    def _parse_termen(self) -> AST:
        nod = self._parse_factor()

        while self._caracter_curent() in ('*', '/'):
            op = self._caracter_curent()
            self._pozitie += 1  # consumam operatorul

            dreapta = self._parse_factor()
            nod = AST(Token(op), nod, dreapta)

        return nod

    def _parse_factor(self) -> AST:
        start = self._pozitie

        while (
            self._caracter_curent() is not None
            and self._caracter_curent().isdigit()
        ):
            self._pozitie += 1

        numar = self._expresie[start:self._pozitie]
        return AST(Token(numar))

    def _caracter_curent(self) -> str | None:
        if self._pozitie < len(self._expresie):
            return self._expresie[self._pozitie]
        return None
