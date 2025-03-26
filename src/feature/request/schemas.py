from typing import Optional
from datetime import datetime
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

class PostSendNews(PostBase):
    seed: str
    text: str
    created_at: datetime

class SendNewsRelationship(PostBase):
    seed: str
    text: str

class PostSendNewsList(PostBase):
    send: list[PostSendNews]

class SelectRelationship(BaseModel):
    news_list: list[SendNewsRelationship]
    current_news: str

class SelectRelationshipResponse(BaseModel):
    seed: Optional[int]

class RelationshipNews(PostBase):
    seed_news: str
    related_new_seed: str

class RelationshipNewsResponse(BaseModel):
    status: str
    seed_news: str
    related_seed: str
    message_id: int

