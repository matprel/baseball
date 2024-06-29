from dataclasses import dataclass

from model.squadra import Squadra

@dataclass
class SalarioS:
    s : Squadra
    salario: float