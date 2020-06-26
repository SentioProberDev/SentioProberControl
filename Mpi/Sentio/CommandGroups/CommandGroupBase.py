from abc import ABC


class CommandGroupBase(ABC):
    def __init__(self, comm):
        self._comm = comm
