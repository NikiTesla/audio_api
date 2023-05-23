from sqlalchemy import (
    MetaData,
    Integer,
    String,
    Table,
    Column,
    create_engine,
    LargeBinary,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values
from tools.token import generate_token

# main database configuration
config = dotenv_values(".env")

engine = create_engine(
    f"postgresql+psycopg2://{config['DB_USER']}:{config['DB_PASSWORD']}"
    + f"@{config['DB_HOST']}:{config['DB_PORT']}/{config['DB_NAME']}"
)
metadata = MetaData()
audio_table = Table(
    "audio_table",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer),
    Column("audio", LargeBinary),
)

users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String),
    Column("token", String),
)
metadata.create_all(engine)

Base = declarative_base()


class Audio(Base):
    __tablename__ = "audio_table"
    id = Column(Integer, primary_key=True, autoincrement=True)
    audio = Column(LargeBinary)
    user_id = Column(Integer)

    def __repr__(self):
        return f"Audio id={self.id}"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True)
    token = Column(String(100), unique=True)

    def __repr__(self):
        return f"User id={self.id}"


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def save_user(username: str) -> dict:
    """
    save_user creates local session, check if User exists.
    In that case returns error message. Else generates token, create user in database and returns it's id and token
    """
    session = SessionLocal()

    user = User(username=username)

    if session.query(User).filter(User.username == username).first() is not None:
        return {"error": "already exists"}

    token = generate_token(username)

    user.token = token
    session.add(user)
    session.commit()
    session.refresh(user)
    session.close()

    return {"user_id": user.id, "token": token, "error": ""}


def save_mp3(token, content) -> dict:
    """
    save mp3 creates local session, checks if user exists. If not returns error message
    """
    session = SessionLocal()

    user = session.query(User).filter(User.token == token).first()
    if user is None:
        return {"error": "no user with such token"}
    user_id = user.id

    audio = Audio(audio=content, user_id=user_id)
    session.add(audio)
    session.commit()
    session.refresh(audio)
    audio_id = audio.id
    session.close()

    return {"audio_id": audio_id, "user_id": user_id, "error": ""}


def get_mp3(audio_id: int, user_id: int):
    """
    get_mp3 search for audio with audio_id and user_id in database. If there is no such audio - returns error message
    """
    session = SessionLocal()

    audio = (
        session.query(Audio)
        .filter(Audio.id == audio_id, Audio.user_id == user_id)
        .first()
    )
    if audio is None:
        return {"error": "audio was not found"}

    return {"raw_audio": audio.audio, "error": ""}
