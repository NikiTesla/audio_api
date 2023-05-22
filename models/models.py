from sqlalchemy import MetaData, Integer, String, Text, Table, Column, create_engine, DateTime, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values
from tools.token import generate_token

config = dotenv_values(".env")

engine = create_engine(f"postgresql+psycopg2://{config['DB_USER']}:{config['DB_PASSWORD']}" + 
                       f"@{config['DB_HOST']}:{config['DB_PORT']}/{config['DB_NAME']}")
metadata = MetaData()
audio_table = Table(
        "audio_table",
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("audio", LargeBinary)
)

users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String),
    Column("token", String)
)
metadata.create_all(engine)

Base = declarative_base()

class Audio(Base):
    __tablename__ = 'audio_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    audio = Column(LargeBinary)

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

def save_user(username: str):
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

def save_mp3(audio: Audio) -> bool:
    session = SessionLocal()
    
    if session.query(Audio).filter(Audio.audio == audio.audio).first() is not None:
        print("exists")
        session.commit()
        return False
    
    session.add(audio)
    session.commit()
    session.close()

    return True