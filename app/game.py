import itertools
from app.models import Player, Game, Round, Result
from app import db


class Choices(object):
    ROCK = 'rock'
    PAPER = 'paper'
    SCISSORS = 'scissors'
    LEAVE_GAME = 'leave'
    INACTIVE = 'inactive'

    def get_all_choices(self):
        return self.get_user_choices() + (self.LEAVE_GAME, self.INACTIVE)

    def get_user_choices(self):
        return self.ROCK, self.PAPER, self.SCISSORS


class Results(object):
    LOSE = 0
    WIN = 1
    TIE = 2


choices = Choices()
results = Results()


class GameRoom(object):
    def __init__(self, team_size=2):
        self.team_size = team_size
        self.game_id = self.set_game_id()
        self.round = 1
        self.round_id = None
        self.is_calculated = False

    @staticmethod
    def set_game_id():
        """Set a room ID to DB"""
        game = Game()
        db.session.add(game)
        db.session.commit()
        game_id = game.id
        db.session.close()
        return game_id

    def add_player(self, player_name, player_sid):
        """Add player into game in DB"""
        player_in_db = Player.query.filter_by(name=player_name).first()
        player = Player(name=player_name, sid=player_sid) if not player_in_db else player_in_db
        print self.game_id
        game = Game.query.get(self.game_id)
        game.players.append(player)
        db.session.add(player)
        db.session.commit()
        db.session.close()

    def is_full_game(self):
        return True if len(self.get_players()) >= self.team_size else False

    def get_players(self):
        game = Game.query.get(self.game_id)
        if game:
            game_players = game.players
            db.session.close()
        else:
            game_players = []
        return game_players

    @staticmethod
    def _get_player_choice(player_id, round_id):
        result_query = Result.query.filter_by(player_id=player_id, round_id=round_id).first()
        if result_query:
            res = result_query.choice
            db.session.close()
            return res

    def get_player_choice_cur_round(self, player_id):
        return self._get_player_choice(player_id, self.round_id)

    def get_opponents_choices(self):
        res = {}
        for player in self.get_players():
            res.update({player.name: self.get_player_choice_cur_round(player.id)})
        return res

    def is_all_choices(self):
        print 'All players', self.get_players()
        for player in self.get_players():
            print player
            if self.get_player_choice_cur_round(player.id) is None:
                print False
                return False
        print True
        return True

    def set_choice(self, player_name, choice):
        """Add player choice to DB"""
        print 'Set choice for player {} - {}'.format(player_name, choice)
        player = Player.query.filter_by(name=player_name).first()
        if not self.round_id:
            cur_round = Round(round=self.round, game_id=self.game_id)
            db.session.add(cur_round)
            db.session.commit()
            print "ROUND", cur_round
            self.round_id = cur_round.id
        else:
            cur_round = Round.query.get(self.round_id)
        result = Result(round_id=cur_round.id, choice=choice, player_id=player.id)
        db.session.add(result)
        db.session.commit()
        db.session.close()

    def __set_player_result(self, player_id, result):
        result_record = Result.query.filter_by(player_id=player_id, round_id=self.round_id).first()
        result_record.result = result
        db.session.add(result_record)
        db.session.commit()
        db.session.close()
        print 'SET RESULT FOR PLAYER {} _ {}'.format(player_id, result)

    def is_all_choices_presented(self):
        for player in self.get_players():
            choice = self.get_player_choice_cur_round(player_id=player.id)
            if not choice:
                return False
        return True

    def get_grouped_users(self):
        res = {}
        for player in self.get_players():
            choice = self.get_player_choice_cur_round(player.id)
            res[choice] = res.get(choice, [])
            res.get(choice, []).append(player)
        print 'RES', res
        return res

    def get_player_result(self, player_name):
        player = Player.query.filter_by(name=player_name).first()
        result_query = Result.query.filter_by(round_id=self.round_id, player_id=player.id).first()
        db.session.close()
        return result_query.result

    def calc_results(self):
        grouped_users = self.get_grouped_users()
        for player in grouped_users.get(choices.LEAVE_GAME, []) + grouped_users.get(choices.INACTIVE, []):
            print 'PLAYER {} leave game'.format(player)
            self.__set_player_result(player.id, results.LOSE)
        for group, players in grouped_users.iteritems():
            if not players or group == (choices.LEAVE_GAME or choices.INACTIVE):
                del grouped_users[group]
        if len(grouped_users) == 1:
            for player in grouped_users[grouped_users.keys()[0]]:
                self.__set_player_result(player.id, results.TIE)
        for group1, group2 in itertools.combinations(grouped_users, 2):
            print group1, group2
            if group1 == choices.ROCK and group2 == choices.PAPER or group1 == choices.PAPER and group2 == choices.SCISSORS or group1 == choices.SCISSORS and group2 == choices.ROCK:
                for player in grouped_users[group1]:
                    self.__set_player_result(player.id, results.LOSE)
                for player in grouped_users[group2]:
                    self.__set_player_result(player.id, results.WIN)
            else:
                for player in grouped_users[group1]:
                    self.__set_player_result(player.id, results.WIN)
                for player in grouped_users[group2]:
                    self.__set_player_result(player.id, results.LOSE)

    @staticmethod
    def get_player_games(player_id):
        player = Player.query.get(player_id)
        return player.games

    def _get_player_all_stats(self, player_id):
        game_res = []
        for game in self.get_player_games(player_id):
            round_res = {}
            for round in game.rounds:
                result = Result.query.filter_by(player_id=player_id, round_id=round.id).first()
                if result:
                    round_res[round.round] = result.result
                else:
                    break
            game_res.append(round_res)
        return game_res

    def get_player_stats(self, player_name):
        res = {}
        player = Player.query.filter_by(name=player_name).first()
        stats = self._get_player_all_stats(player.id)
        for game in stats:
            if game:
                max_round, result = max(game.iteritems(), key=lambda x: x[1])
                res[result] = res.get(result, 0) + 1
        return res
