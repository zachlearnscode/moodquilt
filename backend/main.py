from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, Session, CheckConstraint, SQLModel, create_engine, select, desc
from datetime import date, datetime, timezone, timedelta
from random import randint, choice

origins = ["http://localhost:5173"]

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

class Mood(SQLModel, table=True):    
    user_id: int | None = Field(default=None, primary_key=True, foreign_key="user.id")
    created_at_date: date | None = Field(default=date.fromtimestamp(datetime.now(timezone.utc).timestamp()), primary_key=True)
    last_modified_datetime: datetime | None = Field(default=datetime.now(timezone.utc))
    mood: int = Field(sa_column_args=[CheckConstraint("mood BETWEEN 1 AND 5")])
    note: str | None

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

def seed_tables() -> None:
    with Session(engine) as session:
        # Clear existing data
        session.query(Mood).delete()

        moods = []
        for i in range(0, 1000):
            if choice([0, 1]) == 1:
              moods.append(Mood(
                  user_id=2,
                  created_at_date=date.fromtimestamp(((datetime.now(timezone.utc) - timedelta(days=3)) - timedelta(days=i+1)).timestamp()),
                  mood=randint(1,5)
              ))

        session.add_all(moods)
        session.commit()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    seed_tables()

@app.get("/moods")
def root(session: SessionDep):
    today = date.today()

    statement = select(Mood).order_by(Mood.created_at_date)
    results = session.exec(statement).all()

    weeks = []
    working_week = []
    for i in range(500 + today.weekday()):
        d = today - timedelta(days=i)

        for entry in results:
            if entry.created_at_date == d:
                working_week.insert(0, entry)
                break
        else:
          working_week.insert(0, Mood(mood=0, created_at_date=d))

        if working_week[0].created_at_date.weekday() == 6:
            weeks.insert(0, working_week)
            working_week = []

    return weeks

@app.post("/log")
def log_mood(mood: Mood, session: SessionDep) -> Mood:
    mood.created_at_date = date.fromtimestamp(datetime.strptime(
        mood.created_at_date[:-1],
        "%Y-%m-%dT%H:%M:%S.%f"
      ).timestamp())
    session.add(mood)
    session.commit()
    session.refresh(mood)
    return mood