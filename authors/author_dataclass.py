from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class AuthorDataClass:
    name: Optional[str]
    lastname: Optional[str]
    email: Optional[str]

