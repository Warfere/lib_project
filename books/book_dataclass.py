from dataclasses import dataclass
import datetime
from typing import Optional, Union, List


@dataclass(frozen=True)
class BookDataClass:
    pages: Optional[int]
    date: Optional[datetime.datetime]

    author_id: Optional[int]
    author_name: Optional[str]
    author_lastname: Optional[str]

    title: Optional[str]

    min_pages: int = 0
    max_pages: int = 9999

    min_date: datetime.datetime = datetime.date(1, 1, 1)
    max_date: datetime.datetime = datetime.datetime.now()
