from sqlalchemy.orm import Session

from src.models import init_db


def test_init_db():
    session, engine = init_db()

    assert isinstance(session, Session)
    assert str(engine.url).startswith("postgresql+psycopg2://")

    session.close()
