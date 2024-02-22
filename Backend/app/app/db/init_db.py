from sqlmodel import SQLModel, create_engine, Session
# from core import settings
engine = create_engine("mysql+pymysql://root:2453@localhost/projectmanagement",echo=True)


def create_db_and_table():
    try:
        SQLModel.metadata.create_all(engine)
        print("Tables created successfully")
    except Exception as e:
        print(f"Error creating tables: {e}")


def get_session():
    with Session(engine) as session:
        yield session
