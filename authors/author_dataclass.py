from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class AuthorDataClass:
    name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
