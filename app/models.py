from app import db


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    sid = db.Column(db.String(64))

    def __repr__(self):
        return '<User {}>'.format(self.name)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    players = db.relationship('Player', secondary='game_player_link', lazy='subquery',
        backref=db.backref('games', lazy=True))
    rounds = db.relationship('Round', backref='game', lazy=True)


class Round(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    round = db.Column(db.Integer)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    choice = db.Column(db.Integer)
    result = db.Column(db.Integer)
    round_id = db.Column(db.Integer, db.ForeignKey('round.id'))


game_player_link = db.Table('game_player_link',
                            db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True),
                            db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True)
                           )
