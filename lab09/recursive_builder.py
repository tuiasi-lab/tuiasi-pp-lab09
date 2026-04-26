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
        """Inițializează builder-ul cu starea internă de parsare."""
        self._expresie: str = ""
        self._pozitie: int = 0

    def Parse(self, expresie: str) -> AST:
        """Parsează o expresie aritmetică recursiv.

        Args:
            expresie: Expresia de parsare (ex: "3+5-2").

        Returns:
            Rădăcina arborelui AST.
        """
        self._expresie = expresie
        self._pozitie = 0
        return self._parse_expresie()

    def _parse_expresie(self) -> AST:
        """Parsează o expresie (sumă/diferență de termeni).

        expresie := termen (('+' | '-') termen)*
        """
        stanga = self._parse_termen()

        while self._caracter_curent() in {"+", "-"}:
            op = self._caracter_curent()
            self._pozitie += 1
            dreapta = self._parse_termen()
            stanga = AST(token=Token(op), stanga=stanga, dreapta=dreapta)

        return stanga

    def _parse_termen(self) -> AST:
        """Parsează un termen (produs/câit de factori).

        termen := factor (('*' | '/') factor)*
        """
        stanga = self._parse_factor()

        while self._caracter_curent() in {"*", "/"}:
            op = self._caracter_curent()
            self._pozitie += 1
            dreapta = self._parse_factor()
            stanga = AST(token=Token(op), stanga=stanga, dreapta=dreapta)

        return stanga

    def _parse_factor(self) -> AST:
        """Parsează un factor (număr întreg).

        factor := NUMAR
        """
        start = self._pozitie
        while self._caracter_curent() is not None and self._caracter_curent().isdigit():
            self._pozitie += 1
        numar = self._expresie[start:self._pozitie]
        return AST(token=Token(numar))

    def _caracter_curent(self) -> str | None:
        """Returnează caracterul curent din expresie sau None la sfârșit."""
        if self._pozitie < len(self._expresie):
            return self._expresie[self._pozitie]
        return None
