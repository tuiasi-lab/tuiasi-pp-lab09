"""
Teste pentru Lab 9 — Design Patterns (Singleton, Visitor, AST).

Testele acoperă:
- Vizitatori pre/in/post-ordine
- Evaluatorul AST
- Singleton Log
- RecursiveASTBuilder
"""

import pytest

from lab9.ast_tree import ASTBuilder
from lab9.visitors import (
    VisitPreOrdine,
    VisitInOrdine,
    VisitPostOrdine,
    EvaluatorVisitor,
)
from lab9.log import Log
from lab9.recursive_builder import RecursiveASTBuilder


class TestVisitors:
    """Teste pentru vizitatorii AST."""

    def setup_method(self) -> None:
        """Construiește AST-ul pentru '3+5' înainte de fiecare test."""
        self.builder = ASTBuilder()
        self.ast_3plus5 = self.builder.Parse("3+5")

    def test_pre_ordine_3plus5(self) -> None:
        """Pre-ordine pentru '3+5' trebuie să fie ['+', 3, 5]."""
        vizitator = VisitPreOrdine()
        vizitator.viziteaza(self.ast_3plus5)
        assert vizitator.get_rezultat() == ["+", 3, 5]

    def test_in_ordine_3plus5(self) -> None:
        """In-ordine pentru '3+5' trebuie să fie [3, '+', 5]."""
        vizitator = VisitInOrdine()
        vizitator.viziteaza(self.ast_3plus5)
        assert vizitator.get_rezultat() == [3, "+", 5]

    def test_post_ordine_3plus5(self) -> None:
        """Post-ordine pentru '3+5' trebuie să fie [3, 5, '+']."""
        vizitator = VisitPostOrdine()
        vizitator.viziteaza(self.ast_3plus5)
        assert vizitator.get_rezultat() == [3, 5, "+"]

    def test_pre_ordine_expresie_mai_lunga(self) -> None:
        """Pre-ordine pentru '3+5+2' conține toți operanzii."""
        ast = self.builder.Parse("3+5+2")
        vizitator = VisitPreOrdine()
        vizitator.viziteaza(ast)
        rezultat = vizitator.get_rezultat()
        # Toți operanzii trebuie să fie prezenți
        assert 3 in rezultat
        assert 5 in rezultat
        assert 2 in rezultat
        assert "+" in rezultat

    def test_in_ordine_scadere(self) -> None:
        """In-ordine pentru '10-3' trebuie să fie [10, '-', 3]."""
        ast = self.builder.Parse("10-3")
        vizitator = VisitInOrdine()
        vizitator.viziteaza(ast)
        assert vizitator.get_rezultat() == [10, "-", 3]

    def test_post_ordine_scadere(self) -> None:
        """Post-ordine pentru '10-3' trebuie să fie [10, 3, '-']."""
        ast = self.builder.Parse("10-3")
        vizitator = VisitPostOrdine()
        vizitator.viziteaza(ast)
        assert vizitator.get_rezultat() == [10, 3, "-"]

    def test_rezultat_gol_dupa_init(self) -> None:
        """Vizitator nou are rezultat gol înainte de vizitare."""
        vizitator = VisitInOrdine()
        assert vizitator.get_rezultat() == []


class TestEvaluator:
    """Teste pentru EvaluatorVisitor."""

    def setup_method(self) -> None:
        """Builder AST comun."""
        self.builder = ASTBuilder()

    def test_adunare_simpla(self) -> None:
        """'3+5' = 8."""
        ast = self.builder.Parse("3+5")
        evaluator = EvaluatorVisitor()
        assert evaluator.evalueaza(ast) == 8

    def test_scadere_simpla(self) -> None:
        """'10-3' = 7."""
        ast = self.builder.Parse("10-3")
        evaluator = EvaluatorVisitor()
        assert evaluator.evalueaza(ast) == 7

    def test_inmultire(self) -> None:
        """'3*4' = 12."""
        ast = self.builder.Parse("3*4")
        evaluator = EvaluatorVisitor()
        assert evaluator.evalueaza(ast) == 12

    def test_impartire(self) -> None:
        """'10/2' = 5."""
        ast = self.builder.Parse("10/2")
        evaluator = EvaluatorVisitor()
        assert evaluator.evalueaza(ast) == 5

    def test_prioritate_operatori(self) -> None:
        """'3+5*2' = 13 (nu 16), prioritate înmulțire față de adunare."""
        ast = self.builder.Parse("3+5*2")
        evaluator = EvaluatorVisitor()
        assert evaluator.evalueaza(ast) == 13

    def test_expresie_mai_lunga(self) -> None:
        """'10-3+1' = 8."""
        ast = self.builder.Parse("10-3+1")
        evaluator = EvaluatorVisitor()
        assert evaluator.evalueaza(ast) == 8

    def test_numar_singur(self) -> None:
        """Un singur număr evaluează la el însuși."""
        ast = self.builder.Parse("42")
        evaluator = EvaluatorVisitor()
        assert evaluator.evalueaza(ast) == 42


class TestLog:
    """Teste pentru pattern-ul Singleton Log."""

    def setup_method(self) -> None:
        """Golește mesajele înainte de fiecare test."""
        Log.get_instance().sterge_mesaje()

    def test_singleton_acelasi_obiect(self) -> None:
        """Două apeluri get_instance() returnează același obiect."""
        instanta1 = Log.get_instance()
        instanta2 = Log.get_instance()
        assert instanta1 is instanta2

    def test_singleton_identitate(self) -> None:
        """id() este același pentru toate instanțele."""
        assert id(Log.get_instance()) == id(Log.get_instance())

    def test_log_inregistreaza_mesaj(self) -> None:
        """Mesajul înregistrat apare în lista de mesaje."""
        log = Log.get_instance()
        log.log("Mesaj de test")
        mesaje = log.get_mesaje()
        assert any("Mesaj de test" in m for m in mesaje)

    def test_log_mai_multe_mesaje(self) -> None:
        """Toate mesajele înregistrate sunt păstrate."""
        log = Log.get_instance()
        log.log("Primul")
        log.log("Al doilea")
        log.log("Al treilea")
        assert len(log.get_mesaje()) == 3

    def test_sterge_mesaje(self) -> None:
        """sterge_mesaje() golește lista."""
        log = Log.get_instance()
        log.log("Ceva")
        log.sterge_mesaje()
        assert log.get_mesaje() == []

    def test_mesajele_persista_intre_instante(self) -> None:
        """Mesajele adăugate printr-o referință sunt vizibile prin alta."""
        log1 = Log.get_instance()
        log1.log("Mesaj persistat")
        log2 = Log.get_instance()
        assert any("Mesaj persistat" in m for m in log2.get_mesaje())


class TestRecursiveBuilder:
    """Teste pentru RecursiveASTBuilder."""

    def test_acelasi_rezultat_ca_ast_builder_3plus5(self) -> None:
        """RecursiveASTBuilder produce același rezultat ca ASTBuilder pentru '3+5'."""
        # Rezultat ASTBuilder
        ast_iterativ = ASTBuilder().Parse("3+5")
        ino_iterativ = VisitInOrdine()
        ino_iterativ.viziteaza(ast_iterativ)

        # Rezultat RecursiveASTBuilder
        ast_recursiv = RecursiveASTBuilder().Parse("3+5")
        ino_recursiv = VisitInOrdine()
        ino_recursiv.viziteaza(ast_recursiv)

        assert ino_iterativ.get_rezultat() == ino_recursiv.get_rezultat()

    def test_acelasi_rezultat_3plus5minus2(self) -> None:
        """RecursiveASTBuilder produce același rezultat ca ASTBuilder pentru '3+5-2'."""
        expresie = "3+5-2"

        ast_iterativ = ASTBuilder().Parse(expresie)
        ino_iterativ = VisitInOrdine()
        ino_iterativ.viziteaza(ast_iterativ)

        ast_recursiv = RecursiveASTBuilder().Parse(expresie)
        ino_recursiv = VisitInOrdine()
        ino_recursiv.viziteaza(ast_recursiv)

        assert ino_iterativ.get_rezultat() == ino_recursiv.get_rezultat()

    def test_evaluare_corecta_recursiv(self) -> None:
        """AST-ul construit recursiv evaluează corect."""
        ast = RecursiveASTBuilder().Parse("3+5")
        evaluator = EvaluatorVisitor()
        assert evaluator.evalueaza(ast) == 8

    def test_prioritate_operatori_recursiv(self) -> None:
        """RecursiveASTBuilder respectă prioritatea operatorilor."""
        ast = RecursiveASTBuilder().Parse("3+5*2")
        evaluator = EvaluatorVisitor()
        assert evaluator.evalueaza(ast) == 13

    def test_scadere_recursiv(self) -> None:
        """Scăderea este corectă în versiunea recursivă."""
        ast = RecursiveASTBuilder().Parse("10-3")
        evaluator = EvaluatorVisitor()
        assert evaluator.evalueaza(ast) == 7
