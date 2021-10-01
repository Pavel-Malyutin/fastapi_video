from typing import Optional

import ormar
from ormar import Model, ModelMeta
from db import metadata, database
from datetime import datetime


class Main(ModelMeta):
    metadata = metadata
    database = database


class User(Model):
    class Meta(Main):
        pass

    id: int = ormar.Integer(primary_key=True)
    username: str = ormar.String(max_length=100)


class Video(Model):
    class Meta(Main):
        pass

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=50)
    description: str = ormar.String(max_length=500)
    file: str = ormar.String(max_length=1000)
    user: Optional[User] = ormar.ForeignKey(User)



