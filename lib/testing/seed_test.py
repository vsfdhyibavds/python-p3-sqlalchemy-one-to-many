import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Game, Review, Base
from lib.seed import seed_database

from conftest import SQLITE_URL

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Game, Review, Base
from lib.seed import seed_database

from conftest import SQLITE_URL

@pytest.fixture(scope='class')
def setup_database(request):
    # Setup database connection and create tables
    engine = create_engine(SQLITE_URL)
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)

    # Run seed script logic directly
    session = Session()
    seed_database(session)
    session.close()

    request.cls.Session = Session
    request.cls.engine = engine

    yield

    # Teardown: drop all tables after tests
    Base.metadata.drop_all(engine)

@pytest.mark.usefixtures("setup_database")
class TestSeed:
    '''Test the seeding process'''

    def test_games_count(self):
        session = self.Session()
        games_count = session.query(Game).count()
        session.close()
        assert games_count == 50, f"Expected 50 games, found {games_count}"

    def test_reviews_count_per_game(self):
        session = self.Session()
        games = session.query(Game).all()
        for game in games:
            reviews_count = len(game.reviews)
            assert 1 <= reviews_count <= 5, f"Game {game.id} has {reviews_count} reviews, expected 1-5"
        session.close()
