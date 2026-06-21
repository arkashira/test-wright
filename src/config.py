from dataclasses import dataclass
from enum import Enum
from typing import List

class Framework(Enum):
    PYTEST = "pytest"
    UNittest = "unittest"

@dataclass
class Repository:
    name: str
    url: str

@dataclass
class Config:
    repositories: List[Repository]
    framework: Framework

    def __post_init__(self):
        if not self.repositories:
            raise ValueError("At least one repository must be provided")
        if not self.framework:
            raise ValueError("A framework must be selected")
