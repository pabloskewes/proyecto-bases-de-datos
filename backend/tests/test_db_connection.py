import unittest

from src.database import get_db


class TestDBConnection(unittest.TestCase):
    def test_db_connection(self):
        with get_db() as db:
            self.assertTrue(db)
    