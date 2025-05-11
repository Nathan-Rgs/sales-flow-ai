from common import get_tags
from pydantic import BaseModel, Field

class ClassifierModel(BaseModel):
    tag: str = Field(
        description="Field for defining classes of intention from user's message.",
        enum=get_tags(),
        deprecated=False
    )
