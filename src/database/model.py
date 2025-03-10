from sqlmodel import SQLModel, Field, Session, create_engine
from enum import Enum

import datetime as dt

class Session_Type(Enum):
    libres = "libres"
    qualy = "qualy"
    squaly = "squaly"
    sprint = "sprint"
    carrera = "carrera"

class Users(SQLModel, table=True):
    telephone: str = Field(primary_key=True)
    name: str 
    points: int = 0
    strikes: int = 0

class Teams(SQLModel, table=True):
    id: int|None = Field(primary_key=True, default=None)
    name: str
    user1: str = Field(foreign_key="users.telephone")
    user2: str = Field(foreign_key="users.telephone")

class GP(SQLModel, table=True):
    id: int|None = Field(primary_key=True, default=None)
    name: str
    date_start: dt.date
    date_finish: dt.date

class Sessions(SQLModel, table=True):
    id: int|None = Field(primary_key=True, default=None)
    gp_id: int = Field(foreign_key="gp.id")
    datetime: dt.datetime
    type: Session_Type
    result: str|None = None

class Predictions(SQLModel, table=True):
    id: int|None = Field(primary_key=True, default=None)
    session_id: int = Field(foreign_key="sessions.id")
    user_id: str = Field(foreign_key="users.telephone")
    prediction: str
    points: int|None = None

sqlite_file_name = "database/Porra2025.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

if __name__ == "__main__":
    SQLModel.metadata.create_all(engine)