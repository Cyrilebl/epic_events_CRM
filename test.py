from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Client, Contract, Event

db_user = ""
db_password = ""
db_host = "localhost"
db_port = ""
db_name = ""

db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(db_url)

try:
    conn = engine.connect()

    Base.metadata.drop_all(bind=conn)
    Base.metadata.create_all(bind=conn)

    Session = sessionmaker(bind=conn)
    session = Session()

except Exception as e:
    print(e)
