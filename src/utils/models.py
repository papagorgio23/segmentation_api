from typing import List

from pydantic import BaseModel


class Content(BaseModel):
    memo_text_description: str
    contributor_occupation: str
    contributor_state: str
    first_time_donor: int


class Payload(BaseModel):
    data: List[Content]
