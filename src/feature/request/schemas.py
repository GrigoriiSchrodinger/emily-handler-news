from pydantic import BaseModel


class PostBase(BaseModel):
    pass

class ModifiedPost(PostBase):
    channel: str
    id_post: int
    text: str

class ImproveText(BaseModel):
    text: str
    links: list

class ImproveTextResponse(BaseModel):
    text: str