from sqlalchemy.orm import Session

from src.models import init_db


def test_init_db():
    session = init_db()

    assert isinstance(session, Session)

    session.close()
