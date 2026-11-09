from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    title: str
    due: date
    done: bool = False
