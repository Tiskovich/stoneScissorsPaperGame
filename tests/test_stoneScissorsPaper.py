import pytest
from stoneScissorsPaperGame import on_create
from collections import deque
from app.game import *
from mock import patch
from alchemy_mock.mocking import UnifiedAlchemyMagicMock


class TestGame(object):
    def setUp(self):
        sqLite = UnifiedAlchemyMagicMock()
        self.

    def test_create_game(self):
        game = GameRoom()
        assert isinstance(game, GameRoom)

    def test_game_id_appear_in_db(self):