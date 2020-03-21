import random
import string

STONE = 'stone'
PAPER = 'paper'
SCISSORS = 'scissors'


class Game(object):
    def __init__(self, team_size=2, player=None):
        self.team_size = team_size
        self.game_id = self.generate_room_id()
        self.playerChoices = {player: None} if player else {}

    @classmethod
    def generate_room_id(cls):
        """Generate a random room ID"""
        id_length = 5
        return ''.join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(id_length))

    def add_player(self, player):
        self.playerChoices.update({player: None})

    def is_full(self):
        return True if len(self.playerChoices) >= self.team_size else False

    def is_choices(self):
        return True if None not in self.playerChoices.values() else False

    def set_choice(self, player, choice):
        self.playerChoices[player] = choice

    def get_result(self):
        res = {}
        prev_player = None
        for player, symbol in self.playerChoices.iteritems():
            if not prev_player:
                prev_player = player
                prev_symbol = symbol
            else:
                if symbol == prev_symbol:
                    res.update({player: 'dead_heat', prev_player: 'dead_heat'})
                if symbol == STONE and prev_symbol != PAPER:
                    res.update({player: 'win', prev_player: 'lose'})
                else:
                    res.update({player: 'lose', prev_player: 'win'})
                if symbol == PAPER and prev_symbol != SCISSORS:
                    res.update({player: 'win', prev_player: 'lose'})
                else:
                    res.update({player: 'lose', prev_player: 'win'})
                if symbol == SCISSORS and prev_symbol != STONE:
                    res.update({player: 'win', prev_player: 'lose'})
                else:
                    res.update({player: 'lose', prev_player: 'win'})
        return res
