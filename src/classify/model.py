from common import get_tags
from pydantic import BaseModel, Field

class ClassifierModel(BaseModel):
    tag: str = Field(
        description="",
        enum=get_tags()
    )
