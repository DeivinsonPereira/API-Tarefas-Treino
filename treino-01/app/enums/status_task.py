from enum import Enum


class StatusTask(int, Enum):
    ABERTO: int = 1
    EXECUTANDO: int = 2
    CANCELADO: int = 3
    CONCLUIDO: int = 4
    VENCIDO: int = 5
