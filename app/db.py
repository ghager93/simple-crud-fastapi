from sqlmodel import create_engine, SQLModel, Session

engine = create_engine("sqlite:///instance/app.db", echo=True, pool_pre_ping=True, connect_args={"check_same_thread": False})
test_engine = create_engine("sqlite:///instance/test_app.db", echo=True, pool_pre_ping=True, connect_args={"check_same_thread": False})

def get_session():
    with Session(test_engine) as session:
        yield session