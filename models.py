from typing import Optional
from pydantic import BaseModel

class ItemPayload(BaseModel):
    # the following are attributes/fields of the class
    item_id: Optional[int]
    item_name: str
    quantity: int