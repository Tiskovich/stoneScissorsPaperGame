import random
import string


class Info(object):
    def __init__(self, team_size=2):
        self.team_size = team_size
        self.game_id = self.generate_room_id()
        self.players = []

    @classmethod
    def generate_room_id(cls):
        """Generate a random room ID"""
        id_length = 5
        return ''.join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(id_length))
