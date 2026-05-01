"""
Versiunea recursivă a ASTBuilder.

Construiește AST-ul printr-o funcție recursivă de descent
în loc de abordarea iterativă cu stivă.
"""

from ast import operator

from lab09.ast_tree import AST, Token


class RecursiveASTBuilder:
    """Construiește un AST printr-o funcție recursivă de descendent.

    Gramatică (EBNF):
        expresie  := termen (('+' | '-') termen)*
        termen    := factor (('*' | '/') factor)*
        factor    := NUMAR

    Această gramatică respectă automat prioritatea operatorilor.
    """

    def __init__(self) -> None:
        """Inițializează builder-ul cu starea internă de parsare."""
        self._expresie: str = ""
        self._pozitie: int = 0

    # TODO: Implementează metoda Parse
    def Parse(self, expresie: str) -> AST:
        """Parsează o expresie aritmetică recursiv.

        Produce același AST ca ASTBuilder pentru expresii echivalente.

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

        Returns:
            Nod AST pentru expresia curentă.
        """
        nod = self._parse_termen()
        
        while self._caracter_curent() in {"+", "-"}:
            operator = self._caracter_curent()
            self._pozitie += 1
            dreapta = self._parse_termen()
            nod = AST(token=Token(operator), stanga=nod, dreapta=dreapta)            
        return nod
        # TODO: Parsează primul termen, apoi operatorii + și -

    def _parse_termen(self) -> AST:
        """Parsează un termen (produs/câit de factori).

        Returns:
            Nod AST pentru termenul curent.
        """
        nod = self._parse_factor()
        
        while self._caracter_curent() in {"*", "/"}:
            operator = self._caracter_curent()
            self._pozitie += 1
            dreapta = self._parse_factor()
            # La fel si aici pentru inmultire si impartire:
            nod = AST(token=Token(operator), stanga=nod, dreapta=dreapta)
            
        return nod                   
    # TODO: Parsează primul factor, apoi operatorii * și /

    def _parse_factor(self) -> AST:
        """Parsează un factor (număr întreg).

        Returns:
            Nod AST frunză cu valoarea numerică.
        """
        start = self._pozitie
        while self._caracter_curent() is not None and self._caracter_curent().isdigit():
            self._pozitie += 1
            
        valoare = self._expresie[start:self._pozitie]
        return AST(Token(valoare))
        # TODO: Citește caracterele numerice și creează un nod frunză

    def _caracter_curent(self) -> str | None:
        """Returnează caracterul curent din expresie sau None la sfârșit.

        Returns:
            Caracterul curent sau None.
        """
        if self._pozitie < len(self._expresie):
            return self._expresie[self._pozitie]
        return None
