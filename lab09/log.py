"""
Singleton Log — înregistrează mesaje cu timestamp.

Design Pattern: Singleton
Garantează că există o singură instanță a clasei Log în toată aplicația.
"""

from datetime import datetime
from typing import Optional


class Log:
    """Singleton pentru jurnalizarea mesajelor cu timestamp."""

    _instanta: Optional["Log"] = None

    def __init__(self) -> None:
        self._mesaje: list[str] = []

    @classmethod
    def get_instance(cls) -> "Log":
        """Returnează instanța singleton."""
        if cls._instanta is None:
            cls._instanta = cls()
        return cls._instanta

    def log(self, mesaj: str) -> None:
        """Adaugă mesaj cu timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mesaj_formatat = f"[{timestamp}] {mesaj}"
        self._mesaje.append(mesaj_formatat)

    def get_mesaje(self) -> list[str]:
        return list(self._mesaje)

    def sterge_mesaje(self) -> None:
        self._mesaje.clear()
