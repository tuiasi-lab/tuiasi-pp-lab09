"""
Singleton Log — înregistrează mesaje cu timestamp.

Design Pattern: Singleton
Garantează că există o singură instanță a clasei Log în toată aplicația.
"""

from datetime import datetime
from typing import Optional


class Log:
    """Singleton pentru jurnalizarea mesajelor cu timestamp."""

    # TODO: Adaugă atribut de clasă pentru instanța singleton
    _instanta: Optional["Log"] = None

    def __init__(self) -> None:
        """Inițializează lista de mesaje.

        Nu apela direct — folosește Log.get_instance().
        """
        self._mesaje: list[str] = []

    # TODO: Implementează metoda de clasă get_instance
    @classmethod
    def get_instance(cls) -> "Log":
        """Returnează instanța singleton a clasei Log.

        Dacă instanța nu există, o creează. Apeluri ulterioare
        returnează aceeași instanță.

        Returns:
            Singura instanță a clasei Log.
        """
        raise NotImplementedError("De implementat")

    # TODO: Implementează metoda log
    def log(self, mesaj: str) -> None:
        """Înregistrează un mesaj cu timestamp curent.

        Args:
            mesaj: Mesajul de înregistrat.
        """
        raise NotImplementedError("De implementat")

    def get_mesaje(self) -> list[str]:
        """Returnează lista tuturor mesajelor înregistrate.

        Returns:
            Lista de mesaje cu timestamp.
        """
        return list(self._mesaje)

    def sterge_mesaje(self) -> None:
        """Șterge toate mesajele din jurnal."""
        self._mesaje.clear()
