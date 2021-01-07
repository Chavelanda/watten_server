from app import db


class Stats(db.model):
    __tablename__ = 'stats'

    generation = db.Column(db.Integer, primary_key=True)
    played = db.Column(db.Integer)
    won = db.Column(db.Integer)

    def __init__(self, generation, played, won):
        self.generation = generation
        self.played = played
        self.won = won

    def __repr__(self):
        return '<generation {}, played {}, won {}'.format(self.generation, self.played, self.won)

    def serialize(self):
        return {
            'gen': self.generation,
            'played': self.played,
            'won': self.won,
        }
