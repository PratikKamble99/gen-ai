from typing import List, Optional
from pydantic import BaseModel

class Comment(BaseModel):
    id: int
    content: str
    replies: Optional[List['Comment']] = None

# It forces Pydantic to re-evaluate type annotations that were not defined when the class was initially created (e.g., recursive references).
Comment.model_rebuild()

comment = Comment(
    id=1,
    content="First comment",
    replies=[
        Comment(id=2, content="reply 1"),
        Comment(id=3, content="reply 2"),
    ]
)

print(comment.model_dump())