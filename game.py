import random
import string


class Choices(object):
    ROCK = 'rock'
    PAPER = 'paper'
    SCISSORS = 'scissors'
    LEAVE_GAME = 'leave'


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
        print self.playerChoices
        return True if None not in self.playerChoices.itervalues() else False

    def set_choice(self, player, choice):
        print 'Set choice for player {} - {}'.format(player, choice)
        self.playerChoices[player] = choice

    def _compare_stats(self, choice, opponent_choice):
        res = []
        if choice == choices.ROCK and opponent_choice == choices.SCISSORS:
            res = ['win', 'lose']
        elif choice == choices.ROCK and opponent_choice == choices.SCISSORS:
            res = ['win', 'lose']

    def get_result(self):
        res = {}
        opponent_id = None
        for player, choice in self.playerChoices.iteritems():
            if not opponent_id:
                opponent_id = player
                opponent_choice = choice
            else:
                if choice == opponent_choice:
                    res.update({player: 'dead_heat', opponent_id: 'dead_heat'})
                elif choice == choices.LEAVE_GAME:
                    res.update({player: 'lose', opponent_id: 'win'})
                elif opponent_choice == choices.LEAVE_GAME:
                    res.update({player: 'lose', opponent_id: 'win'})
                elif choice == choices.ROCK and opponent_choice == choices.SCISSORS or\
                        choice == choices.SCISSORS and opponent_choice == choices.PAPER or\
                        choice == choices.PAPER and opponent_choice == choices.ROCK:
                    res.update({player: 'win', opponent_id: 'lose'})
                else:
                    res.update({player: 'lose', opponent_id: 'win'})
        return res


choices = Choices()
